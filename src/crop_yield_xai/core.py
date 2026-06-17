from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


TARGET = "yield_t_ha"
CAT_FEATURES = ["region", "crop"]
ANOMALY_Z_THRESHOLD = -1.0
ANOMALY_STD_DDOF = 1
RANDOM_STATE = 7
EXPECTED_ROWS = 1257
EXPECTED_YEAR_MIN = 1990
EXPECTED_YEAR_MAX = 2025
EXPECTED_CROPS = {"Barley", "Canola", "Oats", "Wheat"}
EXPECTED_DRIVER_GROUPS = ("heat", "drought", "frost_cold", "excess_rain", "radiation")
EVENT_YEARS = (2012, 2021, 2022)
EXPECTED_EVENT_GROUPS = {
    2012: {"heat", "drought"},
    2021: {"heat", "drought"},
    2022: {"heat", "drought", "excess_rain"},
}

NON_WEATHER_COLUMNS = {
    "country",
    "region",
    "crop",
    "year",
    "window",
    "lat",
    "lon",
    TARGET,
    "trend_yield_t_ha",
    "trend_residual_t_ha",
    "trend_residual_z",
    "is_low_yield_anomaly",
    "anomaly_label",
    "predicted_yield_t_ha",
    "predicted_residual_t_ha",
    "residual_observed_minus_predicted",
}

LEAKAGE_TERMS = (
    "trend_",
    "is_low_yield_anomaly",
    "anomaly_label",
    "predicted_yield",
    "predicted_residual",
    "residual_observed",
)


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    frame: Path
    outputs: Path
    figures: Path
    xai_outputs: Path
    xai_figures: Path
    paper: Path
    latex: Path
    paper_figures: Path
    paper_tables: Path
    paper_supplement: Path
    paper_table_csv: Path
    overleaf_zip: Path
    manifest: Path
    reproducibility: Path


def make_project_paths(root: Path) -> ProjectPaths:
    paper = root / "paper"
    latex = paper / "latex_source"
    return ProjectPaths(
        root=root,
        frame=root / "data" / "processed" / "us_model_frame_hemisphere_aware_1990_2025.csv",
        outputs=root / "outputs",
        figures=root / "figures",
        xai_outputs=root / "outputs" / "xai",
        xai_figures=root / "figures" / "xai",
        paper=paper,
        latex=latex,
        paper_figures=latex / "figures",
        paper_tables=latex / "tables",
        paper_supplement=latex / "supplement",
        paper_table_csv=paper / "generated_table_csv",
        overleaf_zip=paper / "overleaf_zip" / "multimethod_xai_crop_yield_anomalies.zip",
        manifest=paper / "DATA_MANIFEST.md",
        reproducibility=paper / "REPRODUCIBILITY.md",
    )


def ensure_xai_dirs(paths: ProjectPaths) -> None:
    paths.xai_outputs.mkdir(parents=True, exist_ok=True)
    paths.xai_figures.mkdir(parents=True, exist_ok=True)


def load_frame(paths: ProjectPaths) -> pd.DataFrame:
    frame = pd.read_csv(paths.frame)
    validate_frame(frame)
    return frame


def validate_frame(frame: pd.DataFrame) -> None:
    if len(frame) != EXPECTED_ROWS:
        raise AssertionError(f"Expected {EXPECTED_ROWS} frame rows, found {len(frame)}")
    if int(frame["year"].min()) != EXPECTED_YEAR_MIN or int(frame["year"].max()) != EXPECTED_YEAR_MAX:
        raise AssertionError("Unexpected year range")
    crops = set(frame["crop"].dropna().unique())
    if crops != EXPECTED_CROPS:
        raise AssertionError(f"Unexpected crops: {sorted(crops)}")
    if frame[TARGET].isna().any():
        raise AssertionError(f"{TARGET} contains missing values")


def weather_columns(frame: pd.DataFrame) -> list[str]:
    return [column for column in frame.columns if column not in NON_WEATHER_COLUMNS]


def full_season_weather_features(frame: pd.DataFrame) -> list[str]:
    stage_suffixes = ("_early", "_mid", "_late")
    features = [
        column
        for column in weather_columns(frame)
        if column != "season_days" and not column.endswith(stage_suffixes)
    ]
    bad = [feature for feature in features if is_leakage_feature(feature)]
    if bad:
        raise AssertionError(f"Leakage-like weather features detected: {bad}")
    return features


def is_leakage_feature(feature: str) -> bool:
    return any(term in feature for term in LEAKAGE_TERMS)


def driver_group(feature: str) -> str:
    if feature in {"rain_sum", "rain_mean"}:
        return "drought"
    if "dry" in feature or "dry_spell" in feature:
        return "drought"
    if "heat" in feature or "heatwave" in feature or feature == "season_tmax_mean":
        return "heat"
    if feature in {"season_tmean_mean", "growing_degree_days_base5"}:
        return "heat"
    if "frost" in feature or "cold" in feature or feature == "min_tmin":
        return "frost_cold"
    if "heavy_rain" in feature or "wet_days" in feature:
        return "excess_rain"
    if feature.startswith("max_") and "rain" in feature:
        return "excess_rain"
    if "radiation" in feature:
        return "radiation"
    if feature == "season_tmin_mean":
        return "frost_cold"
    return "other_weather"


def group_features(features: list[str]) -> dict[str, list[str]]:
    groups = {group: [] for group in EXPECTED_DRIVER_GROUPS}
    unmapped: list[str] = []
    for feature in features:
        group = driver_group(feature)
        if group in groups:
            groups[group].append(feature)
        else:
            unmapped.append(feature)
    if unmapped:
        raise AssertionError(f"Unmapped weather features: {unmapped}")
    return groups


def driver_group_description(group: str) -> str:
    return {
        "heat": "High temperature, heatwave, and growing-degree exposure",
        "drought": "Low rainfall, dry spells, and hot-dry compound stress",
        "frost_cold": "Cold nights, frost days, and low minimum-temperature stress",
        "excess_rain": "Heavy rainfall, wetness, and short-duration rainfall maxima",
        "radiation": "Seasonal solar-radiation anomalies",
    }[group]


def detrend_and_score(frame: pd.DataFrame, threshold: float = ANOMALY_Z_THRESHOLD) -> tuple[pd.DataFrame, pd.DataFrame]:
    pieces: list[pd.DataFrame] = []
    for (_crop, _region), group in frame.groupby(["crop", "region"], sort=True):
        g = group.sort_values("year").copy()
        x = g["year"].to_numpy(dtype=float)
        y = g[TARGET].to_numpy(dtype=float)
        slope, intercept = np.polyfit(x, y, 1)
        trend = slope * x + intercept
        residual = y - trend
        std = np.std(residual, ddof=ANOMALY_STD_DDOF)
        z = np.zeros_like(residual) if not np.isfinite(std) or std == 0 else residual / std
        g["trend_yield_t_ha"] = trend
        g["trend_residual_t_ha"] = residual
        g["trend_residual_z"] = z
        g["is_low_yield_anomaly"] = g["trend_residual_z"] < threshold
        pieces.append(g)
    scored = pd.concat(pieces, ignore_index=True).sort_values(["year", "crop", "region"])
    anomalies = scored[scored["is_low_yield_anomaly"]].copy()
    return scored, anomalies


def model_feature_columns(features: list[str]) -> tuple[list[str], list[str]]:
    return ["lat", "lon"] + features, CAT_FEATURES


def event_key_columns() -> list[str]:
    return ["country", "region", "crop", "year", "window"]


def event_key(row: pd.Series) -> str:
    parts = [str(row[column]) for column in event_key_columns()]
    return "|".join(parts)
