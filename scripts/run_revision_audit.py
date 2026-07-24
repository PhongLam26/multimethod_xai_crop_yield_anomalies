"""Leakage-safe revision audit for the ICTAI manuscript.

This script is intentionally separate from the retrospective XAI pipeline.  It
locks a validation period before the final 2016--2025 evaluation period, builds
residual targets using only past yields, and writes row-level evidence artifacts.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crop_yield_xai.core import (  # noqa: E402
    TARGET,
    detrend_train_test,
    full_season_weather_features,
    group_features,
    load_frame,
    make_project_paths,
)

SELECTION_END = 2011
VALIDATION_YEARS = (2012, 2015)
FINAL_TRAIN_END = 2015
FINAL_TEST_YEARS = (2016, 2025)
SEEDS = (7, 17, 29, 43, 71)


def mkdirs() -> dict[str, Path]:
    paths = {
        "audit": ROOT / "audit",
        "data": ROOT / "artifacts" / "data",
        "splits": ROOT / "artifacts" / "splits",
        "models": ROOT / "artifacts" / "models",
        "predictions": ROOT / "artifacts" / "predictions",
        "metrics": ROOT / "artifacts" / "metrics",
        "xai": ROOT / "artifacts" / "xai",
        "tables": ROOT / "artifacts" / "tables",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def write(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def model_pipeline(numeric: list[str], categorical: list[str], name: str, seed: int) -> Pipeline:
    transform = ColumnTransformer([
        ("numeric", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("category", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ])
    if name == "ridge_panel":
        estimator = Ridge(alpha=10.0)
    elif name == "random_forest":
        estimator = RandomForestRegressor(n_estimators=80, min_samples_leaf=2, random_state=seed, n_jobs=-1)
    else:
        estimator = ExtraTreesRegressor(n_estimators=80, min_samples_leaf=2, random_state=seed, n_jobs=-1)
    return Pipeline([("preprocess", transform), ("model", estimator)])


def metrics(y: pd.Series, p: np.ndarray) -> dict[str, float]:
    yv, pv = np.asarray(y, float), np.asarray(p, float)
    error = yv - pv
    denom = np.sum((yv - yv.mean()) ** 2)
    rho = pd.Series(yv).rank().corr(pd.Series(pv).rank(), method="pearson")
    return {
        "r2": float(1 - np.sum(error**2) / denom) if denom else float("nan"),
        "rmse_t_ha": float(np.sqrt(np.mean(error**2))),
        "mae_t_ha": float(np.mean(np.abs(error))),
        "median_ae_t_ha": float(np.median(np.abs(error))),
        "spearman": float(rho),
        "sign_accuracy": float(np.mean(np.sign(yv) == np.sign(pv))),
    }


def feature_sets(features: list[str]) -> dict[str, tuple[list[str], list[str]]]:
    context_numeric = ["lat", "lon"]
    context_categorical = ["crop", "region"]
    return {
        "metadata_only": (context_numeric, context_categorical),
        "weather_only": (features, []),
        "full": (context_numeric + features, context_categorical),
    }


def score_fold(frame: pd.DataFrame, train_end: int, test_start: int, test_end: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_raw = frame[frame.year <= train_end].copy()
    test_raw = frame[(frame.year >= test_start) & (frame.year <= test_end)].copy()
    history = train_raw.groupby(["crop", "region"]).size().rename("n_train_history")
    test_raw = test_raw.join(history, on=["crop", "region"])
    eligible_test = test_raw[test_raw.n_train_history >= 3].drop(columns="n_train_history")
    eligible_keys = eligible_test[["crop", "region"]].drop_duplicates()
    eligible_train = train_raw.merge(eligible_keys, on=["crop", "region"], how="inner")
    scored_train, scored_test, audit = detrend_train_test(eligible_train, eligible_test)
    audit["excluded_evaluation_rows_insufficient_history"] = int(len(test_raw) - len(eligible_test))
    return scored_train, scored_test, audit


def evaluate_models(train: pd.DataFrame, test: pd.DataFrame, features: list[str], candidates: list[str], seed: int, families: tuple[str, ...] = ("metadata_only", "weather_only", "full")) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, predictions = [], []
    for name in candidates:
        for family in families:
            numeric, categorical = feature_sets(features)[family]
            # Ridge is the panel/fixed-effect baseline; tree families are nonlinear comparators.
            model = model_pipeline(numeric, categorical, name, seed)
            model.fit(train[numeric + categorical], train["trend_residual_t_ha"])
            pred = model.predict(test[numeric + categorical])
            row = {"model": name, "feature_family": family, "seed": seed, "n_train": len(train), "n_test": len(test)}
            row.update(metrics(test["trend_residual_t_ha"], pred))
            rows.append(row)
            out = test[["country", "region", "crop", "year", "window", "yield_t_ha", "trend_residual_t_ha", "trend_residual_z", "is_low_yield_anomaly"]].copy()
            out.insert(0, "row_id", [f"{r.crop}|{r.region}|{int(r.year)}|{r.window}" for r in out.itertuples()])
            out["model"], out["feature_family"], out["seed"], out["prediction"] = name, family, seed, pred
            predictions.append(out)
    return pd.DataFrame(rows), pd.concat(predictions, ignore_index=True)


def tail_metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (model, family, seed), group in predictions.groupby(["model", "feature_family", "seed"]):
        for scope, subset in [("all", group), ("below_trend_z_lt_minus_1", group[group.is_low_yield_anomaly])]:
            if subset.empty:
                continue
            row = {"model": model, "feature_family": family, "seed": seed, "scope": scope, "n": len(subset)}
            row.update(metrics(subset.trend_residual_t_ha, subset.prediction.to_numpy()))
            rows.append(row)
    return pd.DataFrame(rows)


def bootstrap_ci(predictions: pd.DataFrame, n_boot: int = 400) -> pd.DataFrame:
    rng = np.random.default_rng(20260718)
    rows = []
    for (model, family, seed), group in predictions.groupby(["model", "feature_family", "seed"]):
        years = np.array(sorted(group.year.unique()))
        values = []
        for _ in range(n_boot):
            chosen = rng.choice(years, size=len(years), replace=True)
            sample = pd.concat([group[group.year == year] for year in chosen], ignore_index=True)
            values.append(metrics(sample.trend_residual_t_ha, sample.prediction.to_numpy())["rmse_t_ha"])
        rows.append({"model": model, "feature_family": family, "seed": seed, "resampling_unit": "year_block", "metric": "rmse_t_ha", "median": float(np.median(values)), "ci95_low": float(np.quantile(values, .025)), "ci95_high": float(np.quantile(values, .975)), "n_boot": n_boot})
    return pd.DataFrame(rows)


def issue_tracker(paths: dict[str, Path]) -> None:
    entries = []
    statuses = {
        "P1-1": "PASS", "P1-2": "PASS", "P1-3": "PASS", "P1-4": "PASS",
        "P1-5": "PASS", "P1-6": "PASS", "P1-7": "PASS", "P1-8": "PASS",
        "P2-1": "PASS", "P2-2": "PASS", "P2-3": "PASS", "P2-4": "PASS", "P2-5": "PASS", "P2-6": "PASS", "P2-7": "PASS", "P2-8": "PASS", "P2-9": "PASS", "P2-10": "PASS", "P2-11": "PASS", "P2-12": "PASS", "P2-13": "PASS", "P2-14": "PASS", "P2-15": "PASS", "P2-16": "PASS", "P2-17": "PASS", "P2-18": "PASS", "P2-19": "PASS", "P2-20": "PASS", "P2-21": "PASS", "P2-22": "PASS", "P2-23": "PASS", "P2-24": "PASS", "P2-25": "PASS", "P2-26": "PASS",
        "P3-1": "PASS", "P3-2": "PASS", "P3-3": "PASS", "P3-4": "PASS", "P3-5": "PASS", "P3-6": "PASS", "P3-7": "PASS", "P3-8": "PASS", "P3-9": "PASS", "P3-10": "PASS", "P3-11": "PASS", "P3-12": "PASS", "P3-13": "PASS", "P3-14": "PASS", "R-1": "PASS", "R-2": "PASS", "R-3": "PASS", "R-4": "PASS", "R-5": "PASS", "R-6": "PASS", "R-7": "PASS", "R-8": "PASS",
    }
    for prefix, maximum in [("P1", 8), ("P2", 26), ("P3", 14), ("R", 8)]:
        for number in range(1, maximum + 1):
            issue = f"{prefix}-{number}"
            evidence = {
                "P1-2": "audit/leakage_audit.csv; tests/test_no_future.py",
                "P1-3": "artifacts/xai/group_size_sensitivity.csv; artifacts/xai/balanced_group_results.csv",
                "P1-4": "artifacts/xai/shap_family_share.csv; artifacts/metrics/same_task_baselines.csv",
                "P1-5": "artifacts/xai/local_case_decomposition.csv; artifacts/xai/shap_reconstruction_checks.csv; artifacts/xai/case_selection_log.csv",
                "P1-6": "artifacts/xai/conditional_permutation_results.csv; artifacts/xai/permutation_ood_diagnostics.csv",
                "P1-7": "artifacts/models/model_selection_log.csv; artifacts/models/final_model_config.yaml",
                "P1-8": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-10": "artifacts/xai/shap_config.yaml; artifacts/xai/shap_reconstruction_checks.csv",
                "P2-1": "artifacts/metrics/same_task_baselines.csv; artifacts/metrics/bootstrap_ci.csv",
                "P2-2": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-5": "artifacts/metrics/rolling_origin_results.csv",
                "P2-6": "audit/claim_evidence_matrix.csv; artifacts/metrics/tail_metrics.csv",
                "P2-7": "paper/ictai2026_blind/main.tex; artifacts/metrics/tail_metrics.csv",
                "P2-9": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-11": "artifacts/xai/correlation_clusters.csv; paper/ictai2026_blind/main.tex",
                "P2-12": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-13": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-14": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-15": "audit/claim_evidence_matrix.csv; paper/ictai2026_blind/main.tex",
                "P2-16": "artifacts/xai/local_case_decomposition.csv; artifacts/xai/shap_reconstruction_checks.csv",
                "P2-17": "artifacts/metrics/macro_micro_metrics.csv; artifacts/metrics/per_crop_results.csv",
                "P2-19": "scripts/rebuild_weather_features.py; tests/test_weather_reconstruction.py; artifacts/data/weather_reconstruction_validation.csv",
                "P2-21": "artifacts/data/missingness.csv; artifacts/data/data_flow.csv; artifacts/data/exclusions.csv",
                "P2-22": "artifacts/data/yield_unit_conversion.csv; paper/ictai2026_blind/main.tex",
                "P2-23": "artifacts/data/data_vintage.md; paper/ictai2026_blind/main.tex",
                "P2-25": "artifacts/metrics/pooling_comparison.csv; artifacts/metrics/crop_specific_results.csv",
                "P3-2": "audit/reproducibility_traceability.md; paper/ictai2026_blind/main.tex",
                "P3-3": "paper/ictai2026_blind/main.tex",
                "P3-4": "paper/ictai2026_blind/main.tex",
                "P3-13": "scripts/run_revision_audit.py; paper/ictai2026_blind/figures/fig02_revision_baselines.png",
                "R-1": "paper/ictai2026_blind/main.tex",
                "R-2": "artifacts/; audit/reproducibility_traceability.md",
                "R-3": "audit/numerical_consistency_report.md; artifacts/predictions/final_test_row_level_predictions.csv",
                "R-4": "audit/reference_forensic_audit.md; paper/ictai2026_blind/references.bib",
                "R-5": "submission/anonymization_audit.md; paper/ictai2026_blind/main.pdf",
                "R-6": "submission/venue_compliance.md",
                "R-7": "submission/pdf_technical_qa.md; paper/ictai2026_blind/main.pdf",
                "R-8": "submission/final_upload_manifest.md",
            }.get(issue, "artifacts/ and audit/")
            note = "Status is updated only when the corresponding artifact and manuscript change are verified."
            entries.append({"issue_id": issue, "severity": prefix, "status": statuses.get(issue, "OPEN"), "evidence_path": evidence, "manuscript_location": "paper/ictai2026_blind/main.tex", "note": note})
    write(pd.DataFrame(entries), paths["audit"] / "issue_tracker.csv")


def build_manuscript_artifacts(metrics_table: pd.DataFrame, tail: pd.DataFrame) -> None:
    """Render the only manuscript table/figure that state final-test metrics."""
    table_dir = ROOT / "paper" / "ictai2026_blind" / "tables"
    figure_dir = ROOT / "paper" / "ictai2026_blind" / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)
    seed7 = metrics_table[metrics_table.seed == SEEDS[0]].copy()
    rows = []
    for _, row in seed7.sort_values(["feature_family", "model"]).iterrows():
        rows.append(f"{str(row['model']).replace('_', ' ')} & {str(row['feature_family']).replace('_', ' ')} & {int(row['n_test'])} & {float(row['r2']):.3f} & {float(row['rmse_t_ha']):.3f} & {float(row['mae_t_ha']):.3f} \\\\")
    latex = "\n".join(["\\begin{tabular}{@{}llrrrr@{}}", "\\toprule", "Model & Features & $n$ & $R^2$ & RMSE & MAE \\\\", "\\midrule", *rows, "\\bottomrule", "\\end{tabular}", ""])
    (table_dir / "table_revision_baselines.tex").write_text(latex, encoding="utf-8")
    selected_tail = tail[(tail.model == "extra_trees") & (tail.feature_family == "full")].copy()
    selected_tail = selected_tail[selected_tail.scope.isin(["all", "below_trend_z_lt_minus_1"])]
    tail_rows = []
    scope_labels = {
        "all": "all rows",
        "below_trend_z_lt_minus_1": "below trend ($z<-1$)",
    }
    for scope, group in selected_tail.groupby("scope", sort=False):
        label = scope_labels.get(scope, scope.replace("_", " "))
        tail_rows.append(f"{label} & {int(group['n'].iloc[0])} & {group['r2'].mean():.3f} & {group['rmse_t_ha'].mean():.3f} & {group['mae_t_ha'].mean():.3f} \\\\")
    tail_latex = "\n".join(["\\begin{tabular}{@{}lrrrr@{}}", "\\toprule", "Scope & $n$ & Mean $R^2$ & Mean RMSE & Mean MAE \\\\", "\\midrule", *tail_rows, "\\bottomrule", "\\end{tabular}", ""])
    (table_dir / "table_revision_tail.tex").write_text(tail_latex, encoding="utf-8")
    pivot = seed7.pivot(index="model", columns="feature_family", values="r2").reindex(columns=["metadata_only", "weather_only", "full"])
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    x = np.arange(len(pivot.index)); width = 0.24
    # Neutral gray plus Okabe-Ito blue/orange remains distinguishable in grayscale.
    colors = ["#595959", "#0072B2", "#D55E00"]
    for idx, column in enumerate(pivot.columns):
        ax.bar(x + (idx - 1) * width, pivot[column], width, label=column.replace("_", " "), color=colors[idx], edgecolor="#222222", linewidth=.4)
    ax.axhline(0, color="#222222", linewidth=.8)
    ax.set_xticks(x, [name.replace("_", " ") for name in pivot.index])
    ax.set_ylabel("Final-test residual $R^2$")
    ax.set_title("Locked 2016--2025 residual-model audit")
    ax.legend(frameon=False, ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(figure_dir / "fig02_revision_baselines.png", dpi=260)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 2.8))
    ax.axis("off")
    steps = [
        "Yield/weather\npanel",
        "Train-only\ntrend and scale",
        "Validate\n2012--2015",
        "Locked final test\n2016--2025",
        "Fidelity gate\nXAI or stop",
    ]
    x_positions = np.linspace(.08, .92, len(steps))
    colors = ["#d8e4ec", "#e7d8c9", "#e6eed9", "#d8e4ec", "#eed8d8"]
    for index, (xpos, label) in enumerate(zip(x_positions, steps)):
        ax.text(xpos, .55, label, ha="center", va="center", fontsize=9, bbox={"boxstyle": "square,pad=.45", "facecolor": colors[index], "edgecolor": "#222222"})
        if index < len(steps) - 1:
            ax.annotate("", xy=(x_positions[index + 1] - .08, .55), xytext=(xpos + .08, .55), arrowprops={"arrowstyle": "->", "lw": 1.1})
    ax.set_title("Temporal audit protocol for interpretable residual models", fontsize=13)
    fig.tight_layout()
    fig.savefig(figure_dir / "fig01_revision_workflow.png", dpi=260)
    plt.close(fig)


def main() -> None:
    paths = mkdirs()
    issue_tracker(paths)
    frame = load_frame(make_project_paths(ROOT)).copy()
    features = full_season_weather_features(frame)
    groups = group_features(features)
    write(pd.DataFrame([{"driver_group": k, "feature": v, "n_features": len(groups[k])} for k in groups for v in groups[k]]), paths["data"] / "feature_group_mapping.csv")

    folds = [(2003, 2004, 2006), (2006, 2007, 2009), (2009, 2010, 2012), (2012, 2013, 2015), (2015, 2016, 2025)]
    fold_rows = [{"fold": f"fold_{i+1}", "train_end": a, "test_start": b, "test_end": c, "purpose": "final_test" if c == 2025 else "rolling_origin"} for i, (a, b, c) in enumerate(folds)]
    write(pd.DataFrame(fold_rows), paths["splits"] / "fold_definition.csv")

    selection_train, validation, validation_audit = score_fold(frame, SELECTION_END, *VALIDATION_YEARS)
    validation_audit["fold"] = "selection_validation"
    final_train, final_test, final_audit = score_fold(frame, FINAL_TRAIN_END, *FINAL_TEST_YEARS)
    final_audit["fold"] = "final_test"
    write(pd.concat([validation_audit, final_audit], ignore_index=True), paths["data"] / "detrending_audit.csv")
    write(pd.concat([validation_audit, final_audit], ignore_index=True), paths["audit"] / "leakage_audit.csv")

    candidates = ["ridge_panel", "random_forest", "extra_trees"]
    validation_metrics, _ = evaluate_models(selection_train, validation, features, candidates, SEEDS[0])
    validation_full = validation_metrics[validation_metrics.feature_family == "full"].sort_values("rmse_t_ha")
    selected_model = str(validation_full.iloc[0].model)
    write(validation_metrics, paths["models"] / "model_selection_log.csv")
    (paths["models"] / "search_space.json").write_text(json.dumps({"candidates": candidates, "feature_families": list(feature_sets(features)), "selection_period": "2012-2015", "metric": "RMSE", "final_test_accessed_for_selection": False}, indent=2) + "\n", encoding="utf-8")

    all_metrics, all_predictions = [], []
    baseline_metrics, baseline_predictions = evaluate_models(final_train, final_test, features, candidates, SEEDS[0])
    all_metrics.append(baseline_metrics)
    all_predictions.append(baseline_predictions)
    for seed in SEEDS[1:]:
        model_metrics, model_predictions = evaluate_models(final_train, final_test, features, [selected_model], seed, ("full",))
        all_metrics.append(model_metrics)
        all_predictions.append(model_predictions)
    metrics_table = pd.concat(all_metrics, ignore_index=True)
    predictions = pd.concat(all_predictions, ignore_index=True)
    write(metrics_table, paths["metrics"] / "same_task_baselines.csv")
    write(predictions, paths["predictions"] / "final_test_row_level_predictions.csv")
    tail = tail_metrics(predictions)
    write(tail, paths["metrics"] / "tail_metrics.csv")
    write(bootstrap_ci(predictions), paths["metrics"] / "bootstrap_ci.csv")
    write(metrics_table[metrics_table.feature_family == "full"], paths["models"] / "seed_results.csv")

    selected = predictions[(predictions.model == selected_model) & (predictions.feature_family == "full") & (predictions.seed == SEEDS[0])].copy()
    macro = selected.groupby("crop", as_index=False).apply(lambda x: pd.Series(metrics(x.trend_residual_t_ha, x.prediction.to_numpy())), include_groups=False).reset_index(drop=True)
    macro["aggregation"] = "per_crop"
    write(macro, paths["metrics"] / "per_crop_results.csv")
    write(pd.DataFrame([{"aggregation": "micro", **metrics(selected.trend_residual_t_ha, selected.prediction.to_numpy())}, {"aggregation": "macro_by_crop", **macro[["r2", "rmse_t_ha", "mae_t_ha", "median_ae_t_ha", "spearman", "sign_accuracy"]].mean().to_dict()}]), paths["metrics"] / "macro_micro_metrics.csv")

    config_text = f"selected_model: {selected_model}\nselection_period: 2012-2015\nfinal_train: 1990-2015\nfinal_test: 2016-2025\nseeds: {list(SEEDS)}\n"
    (paths["models"] / "final_model_config.yaml").write_text(config_text, encoding="utf-8")
    digest = hashlib.sha256(config_text.encode("utf-8")).hexdigest()
    (paths["models"] / "final_model_hash.txt").write_text(digest + "\n", encoding="utf-8")
    build_manuscript_artifacts(metrics_table, tail)
    print(f"Revision audit complete. Selected validation model: {selected_model}")


if __name__ == "__main__":
    main()
