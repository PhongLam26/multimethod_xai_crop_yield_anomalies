# Extracted Upgrade Plan

- Source: `C:\Users\phong\Downloads\ICTAI_FIX\KE_HOACH_NANG_CAP_PAPER_ICTAI2026_CHO_CODEX_GIU_DATASET_V1.docx`

## Paragraphs

- **Normal**: KẾ HOẠCH NÂNG CẤP TOÀN DIỆN PAPER ICTAI 2026
- **Normal**: Từ một negative-result audit paper thành một nghiên cứu phương pháp + ứng dụng có sức thuyết phục cao
- **Normal**: Bản cập nhật: bảo tồn dataset state-level V1 làm immutable backup/baseline và xây V2 theo hướng mở rộng song song.
- **Normal**: MASTER EXECUTION PLAN FOR CODEX
- **Normal**: Đầu vào hiện tại: paper 8 trang với Gate A/Gate B1/Gate B2, locked test, kết quả dự báo yếu nhưng audit chặt.
Đầu ra mong muốn: một phiên bản paper mới có method contribution được benchmark, application story rõ, dữ liệu tốt hơn, external validation và một candidate model chỉ được chọn bằng quy trình hợp lệ.
- **Heading 1**: 1. Executive summary và nguyên tắc không thương lượng
- **List Bullet**: Freeze bản paper hiện tại thành baseline bất biến, kèm PDF hash, data hash, config hash và tag Git.
- **List Bullet**: Mỗi hướng cải tiến là một branch độc lập, có pre-registration JSON trước khi chạy: câu hỏi, target, split, metric, model grid, pass rule và stop rule.
- **List Bullet**: Không dùng locked 2016–2025 state-level test của paper hiện tại để chọn model mới. Giai đoạn này chỉ dùng làm baseline/audit reference. Dataset state-level hiện tại (V1) phải được giữ nguyên, không xóa, không ghi đè và không biến đổi âm thầm khi xây dataset county-level V2.
- **List Bullet**: Mọi candidate dương phải có một external holdout mới: geography chưa dùng, thời gian chưa dùng trong branch, hoặc domain thứ hai.
- **List Bullet**: Không hợp nhất mọi experiment vào paper. Cuối cùng chọn một câu chuyện chính mạch lạc bằng scoring matrix đã định trước.
- **List Bullet**: Nếu không có model thực tế nào vượt gate trên external holdout, không được bịa “model tốt”; khi đó chọn nhánh method benchmark + application abstention nếu scoring tổng thể đạt chuẩn.
- **Heading 2**: 1.1 Định nghĩa “8/10” để Codex không hiểu sai
- **Normal**: Target paper-readiness score: ≥ 80/100. Không dùng một con số R² duy nhất làm thước đo “8 điểm”.
- **Heading 2**: 1.2 Snapshot baseline phải khóa trước
- **Code Block**: git checkout -b baseline/fidelity-audit-v1
git add -A
git commit -m "Freeze accepted fidelity-audit baseline"
git tag -a baseline-v1.0 -m "Current 8-page ICTAI baseline before expansion"
python scripts/hash_release.py --paper submission/ictai2026_paper_blind.pdf --out audit/baseline_v1_manifest.json
python scripts/data/freeze_legacy_dataset.py \
  --dataset-id state-panel-v1 \
  --processed data/legacy/state_panel_v1/processed/panel.parquet \
  --schema data/legacy/state_panel_v1/schema/feature_dictionary.csv \
  --out data/legacy/state_panel_v1/manifest.json
- **Heading 2**: 1.3 Chính sách bảo tồn dataset cũ (V1) — bắt buộc
- **Normal**: Dataset đang dùng trong paper hiện tại phải được xem là một tài sản nghiên cứu bất biến, không phải dữ liệu tạm sẽ bị thay thế khi xây Agriculture V2. Codex phải giữ V1 để làm bản sao lưu, regression test, benchmark lịch sử và đối chứng trực tiếp với mọi pipeline mới.
- **List Bullet**: Định danh canonical: `state-panel-v1` — 1.257 crop–state–year rows, 1990–2025, Barley/Canola/Oats/Wheat, 12 U.S. states, target train-only và locked-test protocol hiện tại.
- **List Bullet**: Không xóa, rename tùy tiện, overwrite hoặc tái sinh V1 dưới cùng đường dẫn mà không đổi version/hash. Mọi thay đổi schema phải tạo V1.1/V2 mới.
- **List Bullet**: Giữ processed snapshot, row IDs, schema/feature dictionary, unit conversions, crop–state coordinates, split manifests, target-construction config, prediction vectors, bootstrap draws, figures/tables và paper baseline.
- **List Bullet**: Nếu raw USDA/NASA snapshot được phép lưu thì giữ read-only cùng checksum. Nếu không được phân phối, giữ request manifests, access dates, source URLs, downloader version, response hashes và lệnh tái tạo chính xác.
- **List Bullet**: V1 không được trộn âm thầm vào training V2. Nó chỉ được dùng cho baseline reproduction, backward-compatibility tests, transfer/comparison experiments và backup.
- **List Bullet**: So sánh V1–V2 phải ghi rõ unit khác nhau: V1 ở state level, V2 dự kiến ở county level. Chỉ so metric trực tiếp trên một matched evaluation design hoặc sau khi aggregate V2 lên state–crop–year bằng rule được preregister.
- **List Bullet**: Mỗi candidate V2 phải tạo `reports/v1_v2_comparison.md` và JSON tương ứng: coverage, rows, crops, geography, target construction, baselines, Gate A/B1, tail recovery, uncertainty, compute cost và limitations.
- **List Bullet**: Nếu V2 pipeline hỏng hoặc external holdout không khả dụng, V1 vẫn phải reproduce hoàn chỉnh bằng một lệnh và paper baseline vẫn build được.
- **Code Block**: data/legacy/state_panel_v1/
  README.md
  manifest.json
  raw_manifest/              # queries, access dates, source hashes; raw files only if redistributable
  processed/panel.parquet    # immutable processed snapshot
  schema/feature_dictionary.csv
  splits/
  configs/
  predictions/
  bootstrap/
  generated_tables/
  generated_figures/
  paper_baseline/

make legacy-v1-reproduce
make legacy-v1-verify
make compare-v1-v2
- **Heading 1**: 2. Application contribution: paper giải quyết câu chuyện gì, cho ai?
- **Normal**: Contribution ứng dụng phải được viết như một hệ thống hỗ trợ quyết định có khả năng “abstain”, không phải hệ thống tự động gán nguyên nhân thời tiết. Paper nên giải quyết câu hỏi thực tế: “Khi một vùng có sản lượng thấp hơn xu hướng, dữ liệu và model hiện có có đủ đáng tin để cho phép một analyst xem weather explanation hay phải dừng và yêu cầu thêm bằng chứng?”
- **Heading 2**: 2.1 Đối tượng sử dụng chính
- **Heading 2**: 2.2 Workflow ứng dụng đề xuất
- **List Number**: Input: crop, county/state, season, historical yield, weather exposure, crop mask, phenology, soil, drought và irrigation context.
- **List Number**: Predict: residual magnitude hoặc probability của below-trend event trên một thời điểm đã định trước.
- **List Number**: Audit: Gate A kiểm predictive fidelity; Gate B1 kiểm incremental weather value; tail gate kiểm severe-event recovery.
- **List Number**: Decide: INTERPRET khi gate PASS; ABSTAIN khi gate FAIL; NEED MORE DATA khi coverage/scale/history không đủ.
- **List Number**: Output: risk score, prediction interval, event rank, feature groups chỉ khi được phép, reason codes, data gaps, evidence trace.
- **List Number**: Human action: analyst quyết định điều tra, liên hệ extension, so sánh drought/irrigation/soil context; hệ thống không tuyên bố nguyên nhân.
- **Heading 2**: 2.3 Success metrics mang tính ứng dụng
- **Heading 1**: 3. Kiến trúc chương trình nghiên cứu đa nhánh
- **Heading 2**: 3.1 Thứ tự thực thi bắt buộc
- **List Number**: Freeze baseline và tạo pre-registration templates.
- **List Number**: Chạy T1 synthetic benchmark trước: đây là đường nhanh nhất để tăng novelty và có result dương có ground truth.
- **List Number**: Xây T2 Agriculture V2 data pipeline; không chờ toàn bộ data hoàn hảo mới chạy pilot.
- **List Number**: Chạy T3 model families trên development only; chọn candidate bằng nested validation.
- **List Number**: Khi candidate khóa xong mới mở external holdout.
- **List Number**: Chạy T4 external domain nếu T1 tốt hoặc T2 không đủ mạnh; không để T4 làm loãng câu chuyện.
- **List Number**: Xây T5 prototype sau khi output schema của gate/model ổn định.
- **List Number**: Dùng T6 scorecard để chọn phiên bản paper cuối; lưu mọi version có cải thiện trước khi tiếp tục.
- **Heading 2**: 3.2 Quy tắc versioning “cải thiện thì lưu lại rồi làm tiếp”
- **Code Block**: # Mỗi experiment phải có thư mục bất biến
experiments/<exp_id>/
  preregistration.json
  config.yaml
  data_manifest.json
  metrics_validation.json
  metrics_external.json        # chỉ tạo sau freeze
  predictions.parquet
  figures/
  report.md
  decision.json                # promote / reject / blocked

# Ví dụ
python scripts/new_experiment.py --id T2-county-catboost-v1 --parent baseline-v1.0
python scripts/run_experiment.py experiments/T2-county-catboost-v1/config.yaml
python scripts/evaluate_promotion.py experiments/T2-county-catboost-v1
- **Heading 1**: 4. Data plan: nguồn chính thức, cách lấy và vai trò
- **Normal**: Codex phải tạo downloader có cache, checksum, retry, rate-limit, schema validation và data-vintage manifest. Không commit API keys. Mỗi nguồn phải có `source_url`, `access_date`, `license/terms`, `raw_hash`, `processed_hash`, `availability_time` và `leakage_risk`.
- **Heading 2**: 4.1 Môi trường secrets và downloader contract
- **Code Block**: # .env.example — không commit giá trị thật
NASS_API_KEY=
NOAA_CDO_TOKEN=
EIA_API_KEY=

# Required downloader behavior
python scripts/data/download_nass.py --config configs/data/nass_county_yield.yaml
python scripts/data/download_power.py --config configs/data/power_crop_grid.yaml --max-workers 5
python scripts/data/download_usdm.py --config configs/data/usdm_county.yaml
python scripts/data/download_cdl.py --years 2008:2025 --crops corn,soybeans,winter_wheat
python scripts/data/build_data_manifest.py --raw-dir data/raw --out data/manifests/raw_manifest.json
- **Heading 2**: 4.2 Dataset V2 ưu tiên: county-level corn + soybeans + winter wheat
- **Normal**: Agriculture V2 là nhánh mở rộng bổ sung, không thay thế hoặc làm mất dataset V1. Toàn bộ downloader, target builder và evaluation của V2 phải viết sang namespace/path mới; mọi migration chỉ được thực hiện qua script có version và phải giữ khả năng reproduce V1 byte-for-byte hoặc within documented numerical tolerance.
- **Heading 2**: 4.3 Hai chế độ application để tránh claim mơ hồ
- **Heading 1**: 5. Hướng dẫn lấy dữ liệu chi tiết cho Codex
- **Heading 2**: 5.1 USDA NASS Quick Stats — yield, acreage, progress, irrigation
- **List Bullet**: Yêu cầu người dùng lấy API key từ Quick Stats; đọc từ `NASS_API_KEY` và không ghi key vào log.
- **List Bullet**: Trước khi query data, gọi endpoint parameter values để xác minh exact commodity/statistic/unit labels; không hard-code dựa trên trí nhớ.
- **List Bullet**: Lưu mọi request parameters vào `data/requests/nass/<request_id>.json` và response hash.
- **List Bullet**: County yield query phải yêu cầu `agg_level_desc=COUNTY`, `statisticcat_desc=YIELD`, `unit_desc` phù hợp từng crop, `freq_desc=ANNUAL` và `reference_period_desc=YEAR` khi có.
- **List Bullet**: Crop Progress query dùng `source_desc=SURVEY`, program Survey, weekly frequency và stage descriptions; xây stage dictionary từ returned metadata.
- **List Bullet**: Irrigation dùng program Census và chỉ gán latest past census value cho mỗi year.
- **Code Block**: # Pseudocode; script phải discover exact parameter values trước
params = {
  "key": os.environ["NASS_API_KEY"],
  "source_desc": "SURVEY",
  "sector_desc": "CROPS",
  "commodity_desc": crop,
  "statisticcat_desc": "YIELD",
  "agg_level_desc": "COUNTY",
  "year__GE": 2008,
  "year__LE": 2025,
  "format": "JSON",
}
# GET https://quickstats.nass.usda.gov/api/api_GET/?<encoded params>
# Validate: response count, unique units, domain/category descriptors, suppressed values.
- **Heading 2**: 5.2 NASA POWER — crop-area-weighted weather
- **List Bullet**: Tạo grid points/cells giao với county crop mask. Không gọi lặp cùng cell; cache theo rounded POWER grid coordinate.
- **List Bullet**: Ưu tiên Daily API AG community; request T2M_MAX, T2M_MIN, PRECTOTCORR, ALLSKY_SFC_SW_DWN và các biến bổ sung theo feature spec.
- **List Bullet**: Giới hạn tối đa 5 request đồng thời và exponential backoff cho HTTP 429/5xx.
- **List Bullet**: Weather aggregation: tính feature ở từng grid cell rồi weight bằng crop-pixel area share; so sánh với county centroid trong ablation.
- **List Bullet**: Khóa raw response và metadata vì POWER archive có thể được update/bias-correct.
- **Code Block**: BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
  "parameters": "T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
  "community": "AG",
  "longitude": lon,
  "latitude": lat,
  "start": "20080101",
  "end": "20251231",
  "format": "JSON",
  "time-standard": "UTC",
}
# Cache by (POWER grid cell, start, end, parameter set, data version/access date)
- **Heading 2**: 5.3 CDL + county boundaries — crop mask và weighting
- **List Bullet**: Tải CDL annual 2008–2025 từ official National Download/CroplandCROS; ưu tiên state subset hoặc Cloud Optimized GeoTIFF để tránh tải toàn quốc khi pilot.
- **List Bullet**: Download Census TIGER/Line county polygons và chuẩn hóa GEOID/FIPS.
- **List Bullet**: Map CDL class codes cho corn, soybeans, winter wheat bằng metadata từng year; không giả định code ổn định nếu chưa kiểm.
- **List Bullet**: Tính crop area share theo county-year; lưu pixel count, valid area, confidence/coverage flags.
- **List Bullet**: Post-season branch có thể dùng same-year CDL. In-season branch phải dùng mask available before cutoff hoặc trailing crop frequency mask để tránh lookahead.
- **Heading 2**: 5.4 Drought, soil, irrigation và phenology
- **Heading 1**: 6. Track T1 — Synthetic benchmark có ground truth
- **Normal**: Đây là hướng nâng novelty nhanh và an toàn nhất. Mục tiêu không phải chứng minh model crop hiện tại tốt, mà chứng minh fidelity gate thực sự giảm kết luận XAI sai và biết cho phép giải thích khi signal đủ mạnh.
- **Heading 2**: 6.1 Data-generating process
- **Heading 2**: 6.2 Methods compared
- **Heading 2**: 6.3 Primary metrics và pass targets
- **Heading 2**: 6.4 Experiment scale
- **Code Block**: # Minimum benchmark grid
scenario_families = 6
levels_per_family = 3-4
random_seeds = 100
model_families = [Ridge, ExtraTrees, HistGradientBoosting]
xai_methods = [SHAP_or_exact_tree, permutation, grouped_ablation]

# Save every run
synthetic/results/<scenario>/<seed>/<model>/metrics.json
synthetic/results/<scenario>/<seed>/<model>/gate_decision.json
- **Heading 2**: 6.5 Figure/table package
- **List Bullet**: Figure: false-attribution rate vs signal strength for ungated, performance-only and full gate.
- **List Bullet**: Figure: permission coverage vs false-attribution risk.
- **List Bullet**: Figure: leaked full-series detrending creates plausible XAI narrative versus train-only protocol.
- **List Bullet**: Table: gate ablation across no-signal, drift, correlated features and omitted-variable scenarios.
- **List Bullet**: Case panel: true driver, model prediction, XAI narrative, gate decision and reason code.
- **Heading 1**: 7. Track T2 — Agriculture V2: dữ liệu tốt hơn và external holdout mới
- **Heading 2**: 7.1 Câu hỏi nghiên cứu ứng dụng
- **Normal**: Primary RQ: Can crop-area-weighted weather, phenology, drought, soil, and irrigation context support reliable county-level below-trend yield triage on an untouched temporal-geographic holdout?
- **Normal**: Secondary RQ: When the model is not reliable, can the fidelity gate identify data insufficiency and prevent unsupported weather explanations?
- **Heading 2**: 7.2 Split strategy mới — bắt buộc để kết quả có giá trị
- **Normal**: Hash-based state split: Sort state FIPS by SHA-256(seed + FIPS); reserve approximately 25–30% states. Lưu seed và state list trong preregistration trước khi tải outcome holdout.
- **Heading 2**: 7.3 Data build stages
- **List Number**: Pilot 1: 3 states × corn × 2008–2025; validate end-to-end downloader and weighting.
- **List Number**: Pilot 2: 8–12 major states × corn/soy; assess yield coverage, suppression and compute cost.
- **List Number**: Primary build: all eligible major states/counties for corn, soybeans, winter wheat.
- **List Number**: Feature audit: compare centroid weather, crop-area-weighted weather, stage-specific weather and context covariates.
- **List Number**: Legacy comparison: chạy lại protocol V1 nguyên bản; sau đó tạo matched state-level view từ V2 cho các crop/state/year giao nhau để tách lợi ích do độ phân giải, feature mới và population mới.
- **List Number**: Freeze eligible population before external outcome evaluation.
- **Heading 2**: 7.4 Feature sets và ablation
- **Heading 2**: 7.5 Dual-task formulation
- **Heading 2**: 7.6 Promotion rules T2
- **List Bullet**: Gate A overall: upper 95% paired CI of ΔRMSE vs pre-specified baseline < 0 on external holdout.
- **List Bullet**: Gate A tail: primary z<-1 error/rank recovery vượt null; classification PR-AUC improvement over prevalence with uncertainty.
- **List Bullet**: Gate B1: selected weather/context-enhanced model beats metadata-only on identical external rows with CI.
- **List Bullet**: Temporal-geographic robustness: majority development folds improve; external states not dominated by a single state/crop.
- **List Bullet**: Application threshold: recall@10% review budget materially exceeds random and baseline.
- **List Bullet**: No promotion if only one sensitivity population passes while primary population fails.
- **Heading 1**: 8. Track T3 — Modeling, uncertainty và selective explanation
- **Heading 2**: 8.1 Candidate model families
- **Heading 2**: 8.2 Target construction candidates
- **List Bullet**: Train-only OLS linear trend — baseline.
- **List Bullet**: Train-only Huber trend — robust sensitivity.
- **List Bullet**: Hierarchical trend with crop/state/county random effects fit only on training.
- **List Bullet**: Causal spline/piecewise trend using training data only.
- **List Bullet**: Cross-fitted residual target within development folds to reduce overfit in target construction.
- **List Bullet**: Classification target based on training-only standardized residual; never full-series scaling.
- **Heading 2**: 8.3 Model selection — Pareto + nested validation
- **Normal**: Không chọn bằng một composite score tùy tiện nếu có thể. Dùng Pareto filtering rồi tie-break được preregister:
- **List Number**: Remove model không vượt deployable baseline trên mean development folds.
- **List Number**: Remove model có tail ranking không tốt hơn null hoặc calibration quá kém.
- **List Number**: Remove model có instability lớn giữa states/crops/seeds.
- **List Number**: Trong Pareto set, chọn model đơn giản nhất hoặc model có lowest validation RMSE với one-standard-error rule.
- **List Number**: Freeze feature family, hyperparameters, seeds, threshold và gate config trước external.
- **Heading 2**: 8.4 Selective explanation framework
- **Code Block**: permit_explanation(case_or_population) = (
    gate_A_predictive_fidelity
    and gate_B1_incremental_weather_value
    and tail_or_case_uncertainty_is_acceptable
    and data_quality_is_sufficient
    and distribution_shift_is_not_severe
)

if permit_explanation:
    output = {risk, interval, ranked feature groups, evidence trace}
else:
    output = {ABSTAIN, reason_codes, missing_information, recommended_next_check}
- **Heading 2**: 8.5 Reason codes cho ứng dụng
- **Heading 2**: 8.6 Model promotion threshold
- **Heading 1**: 9. Track T4 — External validation ở domain thứ hai
- **Normal**: Mục tiêu là chứng minh fidelity-gated explanation không chỉ là protocol riêng cho crop yield. Ưu tiên EPA air quality vì data chính thức có pre-generated files và không bắt buộc key cho bulk download.
- **Heading 2**: 9.1 Preferred branch: PM2.5 anomaly triage
- **Heading 2**: 9.2 Acquisition
- **List Bullet**: EPA AirData: use pre-generated daily PM2.5 ZIPs or AQS API; store monitor metadata and completeness flags.
- **List Bullet**: NOAA CDO: request token; station/weather joins by nearest station or city aggregate; respect 5 requests/s and 10,000/day.
- **List Bullet**: Alternative: NASA POWER for consistent weather grid if CDO station completeness is a blocker.
- **List Bullet**: Optional wildfire/smoke covariate must be added only with official/reproducible source and availability audit; otherwise treat as omitted-variable scenario.
- **Heading 2**: 9.3 Minimal external-domain success rule
- **List Bullet**: Synthetic benchmark T1 must be complete first, so method hypothesis is not tuned to air-quality result.
- **List Bullet**: Use same gate architecture; only domain-specific metrics/thresholds may differ and must be preregistered.
- **List Bullet**: Demonstrate at least one PASS and one FAIL regime, or show consistent false-permission reduction versus ungated XAI.
- **List Bullet**: If air-quality data engineering exceeds time budget, archive as BLOCKED and use EIA energy demand only if resources remain.
- **Heading 2**: 9.4 Optional EIA energy-demand branch
- **Normal**: EIA Open Data provides hourly balancing-authority demand, forecast demand, generation and interchange. This branch can test whether weather explanations for demand spikes should be permitted. It requires an EIA API key or bulk download and is lower priority than EPA AirData.
- **Heading 1**: 10. Track T5 — Application prototype và evaluation
- **Heading 2**: 10.1 Prototype scope
- **Heading 2**: 10.2 User story cụ thể
- **Heading 2**: 10.3 Evaluation không cần claim deployment
- **Heading 2**: 10.4 Application contribution metrics
- **List Bullet**: Recall severe events at fixed review budget (5%, 10%, 20%).
- **List Bullet**: Number of unsupported explanations prevented.
- **List Bullet**: Analyst time per correctly prioritized severe event.
- **List Bullet**: Abstention reason agreement and perceived trustworthiness.
- **List Bullet**: Fraction of cases requiring additional data versus permitted interpretation.
- **Heading 1**: 11. Ma trận thực nghiệm và tiêu chí quyết định
- **Heading 2**: 11.1 Pre-registration JSON schema
- **Code Block**: {
  "experiment_id": "E06-county-model-grid-v1",
  "parent_tag": "promising-T2-data-v2",
  "research_question": "...",
  "data_snapshot_hash": "...",
  "development_split": {...},
  "external_holdout": {"encrypted_or_hidden_manifest_hash": "..."},
  "target": {...},
  "features": [...],
  "candidate_models": [...],
  "primary_metrics": [...],
  "pass_rules": {...},
  "tie_break": "one-standard-error then simplest model",
  "stop_rules": [...],
  "created_before_outcome_access": true
}
- **Heading 2**: 11.2 Promotion score cho từng branch
- **Normal**: Promising branch: ≥8/12 và không có scientific-integrity failure. Candidate paper branch: ≥10/12 và overall paper score ≥80/100.
- **Heading 2**: 11.3 Model selection cuối cùng
- **List Number**: Tạo Pareto set từ development only.
- **List Number**: Áp dụng pre-specified tie-break; freeze một model duy nhất cho primary application.
- **List Number**: Giữ model khác làm baseline/ablation, không gọi tất cả là proposed models.
- **List Number**: Mở external holdout một lần, chạy fixed config.
- **List Number**: Nếu PASS, tag external-confirmed; nếu FAIL, không “chọn model thứ hai” trên cùng holdout.
- **List Number**: Chọn paper story dựa trên scorecard: method benchmark + applied model nếu cả hai mạnh; method + abstention application nếu real model vẫn FAIL.
- **Heading 1**: 12. Hai kiến trúc paper cuối có thể chọn
- **Heading 2**: 12.1 Route A — Strong applied + method paper (ưu tiên nếu T2 PASS)
- **Heading 2**: 12.2 Route B — Method + safety/application paper (nếu T2 không PASS)
- **Heading 2**: 12.3 Contribution statements theo route
- **Normal**: Route A: We introduce and validate a fidelity-gated selective-explanation protocol and show that crop-area-weighted weather and management context enable reliable county-level anomaly triage on an untouched temporal-geographic holdout. The resulting system supports analyst prioritization while abstaining from unsupported event-driver claims.
- **Normal**: Route B: We introduce a fidelity-gated selective-explanation protocol that substantially reduces false attribution in controlled temporal-panel benchmarks. Agricultural and air-quality case studies show how the protocol converts potentially persuasive but unsupported XAI narratives into auditable abstention decisions for real analysts.
- **Heading 1**: 13. Repository architecture và command contract
- **Code Block**: project/
  configs/
    data/
      legacy_v1.yaml
      agriculture_v2.yaml
    experiments/
    gate/
  data/
    legacy/
      state_panel_v1/      # immutable; never overwritten by V2
        raw_manifest/
        processed/
        schema/
        splits/
        predictions/
        bootstrap/
        paper_baseline/
    v2/
      raw/                 # gitignored if large/restricted
      interim/
      processed/
      manifests/
      requests/
  experiments/
  synthetic/
  src/
    data/
    targets/
    features/
    models/
    evaluation/
    xai/
    gate/
    application/
  scripts/
    data/
      freeze_legacy_dataset.py
      reproduce_legacy_v1.py
      build_agriculture_v2.py
      compare_v1_v2.py
    reproduce_all.py
    run_experiment.py
    evaluate_promotion.py
    build_paper.py
  tests/
  artifacts/
  reports/
  dashboard/
  manuscript/
  submission/
- **Heading 2**: 13.1 One-command targets
- **Code Block**: make legacy-v1-reproduce
make legacy-v1-verify
make baseline-reproduce
make synthetic-benchmark
make agriculture-pilot
make agriculture-development
make compare-v1-v2
make external-evaluation   # requires explicit --unlock token/confirmation
make airquality-case
make prototype-evaluation
make paper-candidate
make audit-all
- **Heading 2**: 13.2 Mandatory tests
- **List Bullet**: Target immutability: future outcomes cannot change prior target.
- **List Bullet**: Legacy dataset immutability: V1 row IDs, schema, processed hash, split hash and baseline predictions match the frozen manifest.
- **List Bullet**: Version isolation: V2 scripts cannot write into `data/legacy/state_panel_v1/`; CI must fail on unauthorized changes.
- **List Bullet**: Feature availability: no feature timestamp after decision cutoff.
- **List Bullet**: External holdout lock: no training/selection code can read holdout labels before unlock.
- **List Bullet**: Row alignment and paired bootstrap.
- **List Bullet**: Crop mask and area-weight sum checks.
- **List Bullet**: County/FIPS crosswalk and duplicate checks.
- **List Bullet**: Unit conversions by crop.
- **List Bullet**: Suppression/missingness handling.
- **List Bullet**: Synthetic ground-truth recovery.
- **List Bullet**: Gate rule unit tests and reason-code correctness.
- **List Bullet**: Generated tables/figures come from artifact records, not typed numbers.
- **List Bullet**: Clean-clone reproduction and secret scan.
- **Heading 2**: 13.3 Compute budgeting
- **Heading 1**: 14. Lộ trình thực thi đề xuất
- **Heading 2**: 14.1 Stop rules tiết kiệm thời gian
- **List Bullet**: CDL/PPOWER pipeline blocked >2 days: fallback to county centroid pilot, nhưng không gọi đó là final applied contribution.
- **List Bullet**: County yield coverage quá thấp: thu hẹp crop/states dựa trên pre-specified coverage rule, không dựa trên model result.
- **List Bullet**: T2 development không vượt baseline sau model families + context ablation: dừng model chasing; ưu tiên T1/T4/T5.
- **List Bullet**: T1 full gate always abstains: redesign threshold/power analysis trên simulation development, giữ independent simulation test grid.
- **List Bullet**: T4 quá nặng: dùng một compact AirData city panel; không mở EIA trừ khi cần.
- **List Bullet**: Paper vượt 8 trang: giữ core evidence, chuyển full tables/data/source details sang anonymous artifact/repo.
- **Heading 1**: 15. MASTER PROMPT — dán nguyên phần này cho Codex
- **Code Block**: Bạn đang làm việc trên repository của nghiên cứu “Auditing Weather-Feature Reliance in Detrended Crop-Yield Models”. Hãy nâng cấp nghiên cứu theo kế hoạch trong tài liệu này, không chỉ chỉnh câu chữ.

MỤC TIÊU:
1) Nâng paper-readiness lên ≥80/100 theo scorecard novelty, rigor, application, external validity, predictive evidence và reproducibility.
2) Formalize fidelity gate thành selective-explanation/abstention framework.
3) Tạo synthetic benchmark có ground truth để đo false attribution và permission power.
4) Giữ nguyên dataset state-level V1 như một immutable backup/baseline, đồng thời xây Agriculture V2 ở county level với crop-area-weighted weather, phenology, drought, soil và irrigation context.
5) Chọn candidate model chỉ bằng development/nested validation; xác nhận đúng một lần trên external temporal-geographic holdout mới.
6) Xây application story cho agricultural risk analysts: anomaly triage, interpret-or-abstain, reason codes và audit trail.
7) Nếu real-data model không PASS, không bịa kết quả; chọn route method benchmark + applied abstention nếu tổng contribution mạnh.

NON-NEGOTIABLE:
- Freeze current paper and the complete state-level dataset/pipeline as baseline-v1.0 with hashes. Never delete or overwrite V1.
- Existing 2016–2025 state-level locked test cannot be reused for new model selection; it remains available only for exact baseline reproduction and preregistered V1–V2 comparison.
- Every experiment needs preregistration.json created before outcome inspection.
- Do not optimize arbitrary R²=0.8; “8/10” refers to total research quality.
- No final-test model switching, no sensitivity promotion, no full-series leakage.
- Save every promising version/tag before continuing; never overwrite evidence, old datasets, split manifests, predictions or generated paper artifacts.
- Any external holdout may be opened once after model/config freeze.

EXECUTION ORDER:
T0 freeze paper + preserve/reproduce V1 → T1 synthetic benchmark → T2 county data pipeline → T3 model/uncertainty → external holdout → T4 second domain if needed → T5 application prototype → T6 paper selection.

DATA SOURCES:
- USDA NASS Quick Stats for county yield, acreage, crop progress and Census/irrigation variables; API key from environment.
- NASA POWER Daily API for weather; cache cells and use ≤5 concurrent requests.
- USDA CDL/CroplandCROS annual crop masks 2008+.
- Census TIGER/Line county polygons.
- U.S. Drought Monitor REST for weekly county drought.
- USDA NRCS gSSURGO/SSURGO for soil; SoilGrids WCS/WebDAV only as fallback because REST may be unavailable.
- NASS Crop Progress weekly data for stage windows.
- Irrigation and Water Management/Census data using latest past survey only.
- EPA AirData/AQS + NOAA/NASA weather for second-domain validation.

MANDATORY DELIVERABLES:
- baseline manifest/tag plus immutable V1 dataset package, reconstruction command and V1 verification report;
- experiment registry with preregistration/config/data hashes;
- synthetic benchmark results and gate ablation;
- county-level data manifest and QA report plus matched V1–V2 comparison report;
- development model grid and promotion decision;
- encrypted/hidden external holdout manifest hash and one-shot evaluation report;
- application prototype and workload/recall metrics;
- route-A/route-B manuscript candidates or a documented choice;
- final scorecard, claim-evidence map, clean reproduction and repository release.

MODEL SELECTION:
Use Pareto filtering on development metrics: deployable-baseline improvement, primary-tail recovery, calibration, stability and simplicity. Apply one-standard-error/simple-model tie-break. Freeze one primary model. External holdout failure cannot be repaired by selecting another model on the same holdout.

PROMOTION:
Tag promising branches that improve preregistered validation metrics without guardrail violations. Tag candidate only when development Gate A/B1 and application/tail rules pass. Tag external-confirmed only after untouched holdout passes.

REPORTING:
After each track, produce report.md with exact commands, runtime, metrics, CIs, hashes, failures, decision and next action. Continue autonomously through the plan until every track is COMPLETE, REJECTED, or BLOCKED with a concrete reason. Do not stop after only creating scaffolding.
- **Heading 2**: 15.1 Báo cáo cuối Codex bắt buộc trả lại
- **List Bullet**: Danh sách branch/tag đã tạo và lý do promote/reject.
- **List Bullet**: Bảng mọi experiment với preregistered metric, validation result, external result và integrity status.
- **List Bullet**: Candidate model cuối: target, features, hyperparameters, split, metrics, CIs, gate status và hash.
- **List Bullet**: Synthetic benchmark headline: false-attribution reduction, permission power và gate ablation.
- **List Bullet**: Data source manifest: source, URL, access date, query, raw/processed hash, license/terms.
- **List Bullet**: Legacy V1 preservation report: canonical path, processed/schema/split hashes, exact reproduce command, byte/numerical comparison with frozen baseline, and V1–V2 matched comparison.
- **List Bullet**: Application story và measured workflow metrics.
- **List Bullet**: Paper route được chọn, score ≥80/100 hay không, và các limitation còn lại.
- **List Bullet**: Final PDF/repository/artifact paths và reproduction status.
- **Heading 1**: Phụ lục A. Official data sources và URL cho downloader
- **Normal**: S1. USDA NASS Quick Stats landing page: https://www.nass.usda.gov/Quick_Stats/
- **Normal**: S2. USDA NASS Developer/API page: https://data.nass.usda.gov/developer/index.php
- **Normal**: S3. NASA POWER Daily API documentation: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- **Normal**: S4. NASA POWER API request tutorials: https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/
- **Normal**: S5. USDA Cropland Data Layer national downloads: https://www.nass.usda.gov/Research_and_Science/Cropland/Release/
- **Normal**: S6. USDA Cropland Data Layer metadata: https://www.nass.usda.gov/Research_and_Science/Cropland/metadata/meta.php
- **Normal**: S7. CroplandCROS portal: https://croplandcros.scinet.usda.gov/
- **Normal**: S8. U.S. Census 2025 TIGER/Line shapefiles: https://www.census.gov/geographies/mapping-files/2025/geo/tiger-line-file.html
- **Normal**: S9. U.S. Drought Monitor data download: https://droughtmonitor.unl.edu/DmData/DataDownload.aspx
- **Normal**: S10. U.S. Drought Monitor REST services: https://www.droughtmonitor.unl.edu/DmData/DataDownload/WebServiceInfo.aspx
- **Normal**: S11. USDA NRCS gSSURGO: https://www.nrcs.usda.gov/resources/data-and-reports/gridded-soil-survey-geographic-gssurgo-database
- **Normal**: S12. USDA NRCS SSURGO/Soil Data Access: https://www.nrcs.usda.gov/resources/data-and-reports/soil-survey-geographic-database-ssurgo
- **Normal**: S13. SoilGrids documentation and access status: https://docs.isric.org/globaldata/soilgrids/index.html
- **Normal**: S14. SoilGrids WebDAV access: https://docs.isric.org/globaldata/soilgrids/WebDav.html
- **Normal**: S15. NASS Crop Progress and Conditions: https://www.nass.usda.gov/Surveys/Guide_to_NASS_Surveys/Crop_Progress_and_Condition/
- **Normal**: S16. NASS Crop Progress gridded layers: https://www.nass.usda.gov/Research_and_Science/Crop_Progress_Gridded_Layers/
- **Normal**: S17. NASS Crop Progress charts/metadata: https://data.nass.usda.gov/Charts_and_Maps/Crop_Progress_%26_Condition/
- **Normal**: S18. NASS Irrigation and Water Management survey: https://data.nass.usda.gov/Surveys/Guide_to_NASS_Surveys/Farm_and_Ranch_Irrigation/
- **Normal**: S19. 2023 Irrigation and Water Management CSV/report tables: https://data.nass.usda.gov/Publications/AgCensus/2022/Online_Resources/Farm_and_Ranch_Irrigation_Survey/
- **Normal**: S20. USDA Census of Agriculture: https://www.nass.usda.gov/AgCensus/
- **Normal**: S21. EPA AirData pre-generated downloads: https://aqs.epa.gov/aqsweb/airdata/download_files.html
- **Normal**: S22. EPA AQS API documentation: https://aqs.epa.gov/aqsweb/documents/data_api.html
- **Normal**: S23. NOAA NCEI Climate Data Online API: https://www.ncei.noaa.gov/cdo-web/webservices/getstarted
- **Normal**: S24. EIA Open Data API: https://www.eia.gov/opendata/index.php/api
- **Heading 1**: Phụ lục B. Data availability facts cần Codex ghi vào manifest
- **Heading 1**: Phụ lục C. Final stop checklist
- **List Bullet**: [ ] Baseline tag/hash/reproduction PASS.
- **List Bullet**: [ ] Dataset V1 is preserved under an immutable legacy path with manifest, schema, row/split hashes and exact reconstruction command.
- **List Bullet**: [ ] V2 never overwrites V1; CI/version-isolation test PASS; matched V1–V2 comparison report exists.
- **List Bullet**: [ ] Every experiment has preregistration created before outcome access.
- **List Bullet**: [ ] Synthetic benchmark includes independent test seeds/scenarios.
- **List Bullet**: [ ] County data source/query/hash/availability manifests complete.
- **List Bullet**: [ ] External state/time holdout was hidden and opened once.
- **List Bullet**: [ ] No selected model was changed after external result.
- **List Bullet**: [ ] Candidate result passes pre-specified Gate A/B1 and application/tail rules, or paper uses honest method-abstention route.
- **List Bullet**: [ ] Application user, decision, workflow, output, reason codes and evaluation are explicit.
- **List Bullet**: [ ] Paper route scores ≥80/100 and tells one coherent story.
- **List Bullet**: [ ] Clean clone reproduction, secret scan, anonymous submission package and GitHub release PASS.

## Table 1

MỤC TIÊU CHẤT LƯỢNG
Mục tiêu là nâng chất lượng nghiên cứu tổng thể lên mức khoảng 8/10 hoặc cao hơn về novelty, rigor, application value, external validity, reproducibility và clarity. Không được ép R² hoặc một metric bất kỳ đạt “0.8”, không được chọn model bằng final test, và không được thay đổi protocol sau khi đã xem kết quả chỉ để tạo kết quả dương.

## Table 2

NGUYÊN TẮC KHOA HỌC BẮT BUỘC
Codex phải tối ưu chất lượng nghiên cứu, không tối ưu kết quả final test. Kết quả “đáng kể” chỉ được công nhận khi được chọn trên development/validation và xác nhận một lần trên external holdout chưa từng dùng để ra quyết định.

## Table 3

Trục đánh giá | Trọng số | Điều kiện để đạt mức mạnh
Novelty phương pháp | 20 | Fidelity gate được formalize thành selective-explanation/abstention framework và có benchmark ground truth.
Độ chặt thực nghiệm | 20 | Nested temporal/geographic evaluation, uncertainty, ablation, null tests, không leakage.
Giá trị ứng dụng | 20 | Có người dùng, quyết định, workflow, output và workload/triage metric rõ.
External validity | 15 | Ít nhất một external geographic holdout hoặc domain thứ hai.
Predictive evidence | 15 | Gate A và Gate B1 PASS trên holdout mới, hoặc method benchmark cho kết quả dương mạnh nếu real-data branch không PASS.
Reproducibility | 10 | One-command reproduction, versioned data manifest, clean clone PASS, claim-evidence map.

## Table 4

Artifact baseline | Giá trị/ý nghĩa
Paper hiện tại | 8 trang; negative-result audit; Gate A và Gate B1 FAIL.
Selected model | ExtraTrees, Weather only, min_samples_leaf=1; selected bằng validation.
Locked test headline | R² ≈ -0.014; RMSE ≈ 0.669 t/ha; ΔRMSE vs zero ≈ -0.005, CI cắt 0.
Primary tail | z < -1; rank/top-10 recovery không vượt null.
Current strength | Leakage-safe protocol, honest abstention, reproducibility framing.
Current weakness | Không có predictive result mạnh; method chưa được benchmark trên known ground truth; application story còn thiên audit.

## Table 5

Người dùng | Quyết định thực tế | Giá trị hệ thống
State departments of agriculture / USDA analysts | Ưu tiên crop-county-year nào cần điều tra sâu sau mùa vụ. | Triage hàng trăm event thành danh sách có uncertainty, evidence và lý do abstain.
Agricultural extension services | Xác định vùng cần trao đổi với nông dân hoặc kiểm tra điều kiện canh tác. | Không biến feature attribution thành causal claim; chỉ cung cấp evidence-ranked cases.
Crop-insurance / risk analysts | Xác định hồ sơ/vùng có weather signal đáng kiểm tra thêm. | Giảm false narrative và hỗ trợ audit trail; không thay thế loss adjustment.
Agribusiness supply-risk teams | Ước lượng vùng nguyên liệu có rủi ro thấp sản lượng. | Early/post-season screening với confidence và data-quality flags.
Climate service researchers | Đánh giá khi nào một XAI narrative được phép công bố. | Reusable fidelity gate cho scientific ML có temporal target.

## Table 6

Metric | Định nghĩa | Mục tiêu development (không phải guarantee)
Workload reduction | Tỷ lệ event analyst cần xem sau triage. | Giảm ≥50% workload trong khi giữ recall severe events.
Recall@budget | Recall top severe events khi chỉ review 10% hoặc 20% case. | Tốt hơn random/null có CI và permutation significance.
False-permission rate | Gate cho phép interpretation khi ground truth/model fidelity không đủ. | Giảm đáng kể so với ungated XAI trong synthetic benchmark.
Abstention utility | Tỷ lệ từ chối đúng trong weak-signal/drift/leakage scenarios. | Cao khi model không đủ tốt nhưng không quá bảo thủ khi signal mạnh.
Calibration | Observed event rate theo probability bin. | Brier/ECE và reliability plot tốt hơn baseline.
Traceability | Tỷ lệ output có thể truy ngược artifact/config/data snapshot. | 100% headline claims.

## Table 7

CÂU CONTRIBUTION ỨNG DỤNG DỰ KIẾN
We develop an uncertainty-aware agricultural anomaly triage system that decides when weather-based explanations are evidentially permitted and when the system must abstain. The system is designed for analysts who prioritize crop-county-season cases for investigation, not for automated causal attribution or farm-level loss decisions.

## Table 8

Track | Mục tiêu | Kết quả dương mong đợi | Vai trò trong paper cuối
T0 — Freeze & preregister | Khóa baseline, split, metrics và integrity rules. | Không leakage/cherry-pick. | Bắt buộc.
T1 — Synthetic benchmark | Chứng minh gate giảm false attribution trên known ground truth. | Method result mạnh, không phụ thuộc real dataset. | Core method contribution.
T2 — Agriculture V2 | County-level, crop-weighted, phenology/soil/drought/irrigation. | Gate A/B1 có khả năng PASS trên external holdout. | Core applied case.
T3 — Modeling & selective explanation | Hierarchical, boosting, classification, conformal/uncertainty. | Candidate model ổn định và gate-aware. | Model evidence, không claim thuật toán mới.
T4 — External domain | EPA air quality hoặc EIA energy demand. | Chứng minh protocol generalizes. | External validity.
T5 — Application prototype | Triage dashboard + abstention + audit trail. | Workload/use-case metrics. | Application contribution.
T6 — Integration & paper selection | Chọn một coherent manuscript bằng scorecard. | Paper ≥80/100 readiness. | Final manuscript.

## Table 9

Trạng thái | Điều kiện | Git action
baseline | Bản hiện tại đã khóa. | tag baseline-v1.0
experiment | Một thay đổi duy nhất, preregistered. | branch exp/<track>-<slug>
promising | Cải thiện validation theo primary metric và không làm hỏng guardrails. | tag promising-<track>-vX
candidate | PASS mọi development gate và đã freeze config. | tag candidate-<track>-vX
external-confirmed | PASS external holdout theo rule định trước. | tag external-confirmed-vX
paper-candidate | Scorecard ≥80/100 và coherent contribution. | branch paper/candidate-vX
rejected | Không cải thiện hoặc violation. | lưu report + tag rejected-<track>-vX; không xóa kết quả.

## Table 10

Nguồn | Biến | Cách lấy | Ghi chú leakage/ổn định
USDA NASS Quick Stats [S1–S2] | County/state yield, acreage, crop progress, Census variables. | API key hoặc bulk .gz; query theo commodity, agg level, year, geography. | API key trong env; lưu query JSON; kiểm suppression và unit.
NASA POWER Daily API [S3–S4] | TMAX/TMIN, precipitation, radiation, humidity/wind nếu cần. | REST daily point/regional; CSV/JSON/NetCDF; ≤5 concurrent requests. | Archive được cập nhật; hash snapshot và ghi data version/access date.
USDA CDL/CroplandCROS [S5–S7] | Annual crop masks, crop area share, crop-weighting. | National/state Cloud Optimized GeoTIFF; 2008+ national coverage. | Annual mask dùng cùng năm chỉ khi available trước prediction cutoff; nếu post-season audit thì ghi rõ.
US Census TIGER/Line [S8] | County polygons/FIPS. | Download annual county shapefile/geopackage. | Khóa geography vintage; xử lý county boundary changes.
US Drought Monitor REST [S9–S10] | Weekly D0–D4 share, DSCI at county/state. | REST CSV/JSON by county FIPS and date range. | USDM bắt đầu 2000; dùng weeks trước cutoff.
USDA NRCS gSSURGO/SSURGO [S11–S12] | Soil texture, AWC, drainage, organic matter, depth. | State gSSURGO/SSURGO download or Soil Data Access. | Static covariates; crop-area-weighted aggregation.
SoilGrids [S13–S14] | Fallback global soil covariates. | WCS/WebDAV; REST API đang không ổn định/paused. | Không phụ thuộc REST; pin files/coverage and hashes.
NASS Crop Progress [S15–S17] | Planting, emergence, flowering/reproductive, maturity, harvest windows. | Quick Stats weekly state data; gridded 2015+ for corn/soy/cotton/winter wheat. | Stage window chỉ dùng information available by forecast date.
Irrigation & Water Management/Census [S18–S20] | Irrigated acres, water applied, irrigation systems. | Quick Stats Census; CSV tables 2003/08/13/18/23. | Dùng latest past census only; không interpolate từ future census.
EPA AirData/AQS [S21–S22] | Second-domain daily PM2.5/ozone anomalies. | Pre-generated ZIP or AQS API. | AQS finalized data có lag; phù hợp retrospective/forecast protocol tùy cutoff.
NOAA NCEI CDO [S23] | Weather for second domain. | API token, 5 req/s, 10k/day. | Token env; station coverage audit.
EIA Open Data [S24] | Optional hourly electricity demand. | API key/bulk operating data. | Optional domain if air-quality branch blocked.

## Table 11

Thiết kế | Quyết định
Spatial unit | County × crop × year; FIPS-stable crosswalk.
Crops phase 1 | Corn, soybeans, winter wheat. Lý do: county yield coverage lớn; CDL/Crop Progress hỗ trợ tốt hơn.
Time | 2008–2025 cho annual CDL masks; có thể có long-history auxiliary branch nhưng không trộn primary.
Outcome | Train-only detrended yield residual và event probability z<-1; raw residual regression + classification dual task.
Feature timing | Post-season diagnostic version trước; in-season version chỉ dùng dữ liệu đến forecast date.
Population filter | County-crop series ≥8 historical observations cho primary; 3/5 là sensitivity.
Suppression | Không impute suppressed yield bằng spatial neighbors trong primary; track missing/suppressed explicitly.
External holdout | Hash-based states + latest years, khóa trước download/inspection.

## Table 12

Mode | Dữ liệu tại thời điểm quyết định | Application claim hợp lệ
Post-season forensic triage | Final yield + season-complete weather, drought, crop progress. | Ưu tiên event cần điều tra; không phải early warning.
In-season risk screening | Weather/progress chỉ đến một cutoff (ví dụ flowering hoặc mid-season); yield chưa biết. | Early screening cho analyst, cần separate target/split/model.

## Table 13

ƯU TIÊN THỰC THI
Làm post-season county-level branch trước để giảm rủi ro data engineering. Chỉ mở in-season branch khi pipeline phenology và availability-time audit đã PASS.

## Table 14

Nguồn | Feature engineering bắt buộc
USDM | Season mean/max DSCI; weeks D1+, D2+, D3+; stage-specific drought share; compound heat+drought weeks.
gSSURGO/SSURGO | AWC 0–30/100cm, clay/sand, drainage, hydrologic group, depth-to-restrictive-layer; crop-area weighted.
SoilGrids fallback | Use WCS/WebDAV, not paused REST API; median/Q0.5 layers at standard depths; record uncertainty if used.
Irrigation | Irrigated-acre share, water applied per irrigated acre, irrigation system mix; latest past survey only.
Crop Progress | Stage dates from cumulative percentages: first crossing 10%, 50%, 90%; interpolate between weekly reports; state-to-county mapping documented.

## Table 15

Scenario family | Biến điều khiển
Signal strength | none, weak, medium, strong; nonlinear heat/drought effects.
Feature correlation | independent; correlated within group; proxy feature; redundant feature.
Omitted variables | management/irrigation confounder hidden or observed.
Temporal drift | stable; coefficient drift; abrupt regime shift; changing crop distribution.
Target construction | train-only detrend; full-series leaked detrend; noisy residual scale.
Sample structure | states/counties/crops/years; balanced/unbalanced panels; missingness.
Model misspecification | linear truth vs tree model; nonlinear truth vs linear model.

## Table 16

Method | Permission rule
Ungated XAI | Luôn diễn giải SHAP/LIME/grouped importance.
Overall-only gate | Chỉ yêu cầu overall RMSE improvement.
Tail-aware Gate A | Overall + primary-tail error/rank/top-k.
Gate A + Gate B1 | Predictive fidelity + incremental feature-family value.
Full selective-explanation gate | Gate A + B1 + uncertainty + drift/history checks.

## Table 17

Metric | Cách tính | Promotion target
False attribution rate | Tỷ lệ run được phép diễn giải nhưng top driver sai hoặc không có true driver. | Full gate giảm ≥50% tương đối so với ungated; CI không chứa 0 cho improvement.
Permission power | Tỷ lệ run signal strong/adequate fidelity được gate cho phép. | Không quá bảo thủ; report curve, target ≥70% trong strong-signal scenarios.
Driver recovery | Top-1/top-k precision, group rank correlation với ground truth. | Tốt hơn ungated conditional on permission.
Abstention accuracy | Đúng khi từ chối weak/no-signal/leakage/drift. | Tốt hơn overall-only gate.
Coverage-risk curve | False attribution theo fraction of cases permitted. | Full gate Pareto-dominates hoặc rõ trade-off.

## Table 18

PROMOTION RULE T1
Promote T1 thành core contribution nếu full gate giảm false attribution có ý nghĩa thống kê trong phần lớn weak/leakage/drift scenarios và vẫn giữ permission power chấp nhận được trong strong-signal scenarios. Không promote nếu gate chỉ từ chối mọi thứ.

## Table 19

Partition | Rule | Quyền sử dụng
Development train | 2008–2018, development states. | Fit target/model.
Development validation | 2019–2021, development states. | Hyperparameter/model/feature selection.
Development audit | Rolling-origin folds trong 2008–2021. | Stability; không thay external.
External temporal-geographic holdout | 2022–2025 trong holdout states được chọn bằng hash trước khi query outcomes. | Mở đúng một lần sau model freeze.
Optional external crop | Một crop chưa dùng trong development. | Transfer test, không model selection.

## Table 20

Feature family | Examples | Role
Metadata/context | crop, county/state, lat/lon, year/history depth. | Baseline.
Crop-weighted weather | stage heat degree-days, frost days, precip totals/extremes, radiation. | Primary incremental family.
Phenology | planting/emergence/reproductive/maturity/harvest crossing dates. | Timing sensitivity.
Drought | USDM DSCI/D1–D4 exposure by stage. | Operational drought context.
Soil | AWC, texture, drainage, depth. | Static resilience context.
Irrigation | irrigated share, water applied, system type. | Management/resilience proxy.
Remote sensing optional | VegScape NDVI/Crop-CASMA soil moisture. | Only if availability and compute allow; separate ablation.

## Table 21

Task | Target | Primary metrics
Residual regression | Raw train-only detrended residual. | RMSE/MAE Δ vs deployable baselines; Spearman; calibration/interval coverage.
Event classification | z<-1 primary; z<-1.5/-2 sensitivity. | PR-AUC, Brier, recall@budget, F1, calibration.
Severe-event ranking | Rank most negative residuals. | NDCG@k, recall@k, top-k lift vs random, permutation p.

## Table 22

KHÔNG ĐƯỢC “CHỌN MODEL TỐT NHẤT” TRÊN EXTERNAL
Nếu external holdout FAIL, lưu version và report. Không quay lại đổi model rồi mở lại holdout. Muốn iteration tiếp theo phải tạo external holdout khác hoặc coi đó là exploratory follow-up, không gọi independent confirmation.

## Table 23

Nhóm | Models | Lý do
Deployable baselines | zero residual; training mean; crop-county rolling mean; previous residual. | Đánh giá giá trị thực, không chỉ test-mean R².
Linear/statistical | Ridge, ElasticNet, GAM/splines, mixed-effects trend/residual model. | Interpretability và hierarchical structure.
Tree boosting | HistGradientBoosting, XGBoost/LightGBM nếu dependency hợp lệ, CatBoost. | Nonlinearity, categorical handling.
Bagging | Random Forest, ExtraTrees. | Continuity với baseline paper.
Uncertainty | Quantile boosting, conformal intervals, calibrated classifier. | Application abstention và risk.
Hierarchical/multitask | Crop-specific heads, state/county random effects, pooled + interactions. | Borrow strength across sparse series.

## Table 24

Code | Meaning
A0 | Overall predictive fidelity not established.
A1 | Primary-tail recovery not established.
B1 | Weather does not add reliable value over metadata/context.
D0 | Insufficient history or unstable residual scale.
D1 | Missing/suppressed outcome or low crop-mask coverage.
S0 | Geographic/temporal distribution shift detected.
U0 | Prediction interval too wide / low confidence.

## Table 25

MODEL “ĐÁNG KỂ”
Một model chỉ được gọi là candidate đáng kể khi PASS Gate A + Gate B1 trên development và được xác nhận trên external holdout; tail/application metrics cũng phải vượt null. Không dùng R² dương rất nhỏ hoặc một CI thuận lợi ở sensitivity population làm “kết quả tốt”.

## Table 26

Thành phần | Thiết kế
Outcome | Daily PM2.5 concentration/anomaly at monitors or county/city aggregate.
Predictors | Weather from NOAA NCEI or NASA POWER, calendar, wildfire proxy optional, site metadata.
Unit | Monitor-day or city-day; select stable monitors with coverage threshold.
Task | Predict daily anomaly/severe high-PM2.5 events and decide whether meteorological explanation is permitted.
Split | Train early years; validation middle years; external holdout cities + latest years.
Application | Environmental analysts prioritize high-risk days/locations; gate abstains under drift or omitted wildfire source.

## Table 27

Screen | Nội dung
Portfolio overview | Map/table crop-county-season; predicted risk; interval; gate status; reason code.
Case detail | Observed/predicted residual, history, weather exposure, context, data quality.
Evidence panel | Gate A/B1/tail metrics, external coverage, distribution-shift flags.
Explanation panel | Chỉ mở khi permit; feature groups, signed contributions, uncertainty, method agreement.
Abstention panel | Lý do không cho phép diễn giải; đề xuất dữ liệu cần bổ sung.
Audit export | JSON/PDF case report with model/data/config hashes.

## Table 28

USER STORY
As a state agricultural risk analyst, I want to rank county-crop seasons with unusually low yields and know whether weather-based explanations are trustworthy, so that I can focus expert investigation on high-priority cases without presenting unsupported causal narratives.

## Table 29

Evaluation | Cách làm
Task-based offline study | So sánh analyst workflow với danh sách ungated vs gated; đo time, cases reviewed, severe-event recall.
Scenario evaluation | Synthetic/real cases gồm true signal, weak signal, drift và missing data; kiểm quyết định interpret/abstain.
Usability heuristic | 5–10 người có nền tảng ML/agriculture nếu có; nếu không, structured expert walkthrough, ghi rõ limitation.
Audit completeness | 100% case report có data/model/config hash và reason codes.

## Table 30

ID | Experiment | Primary outcome | Promote khi
E00 | Freeze baseline | Hashes + reproduction PASS. | All artifacts immutable.
E01 | Synthetic no-signal/weak/strong | False attribution + permission power. | Full gate beats ungated and is not always-abstain.
E02 | Synthetic leakage/detrending | False narrative under full-series vs train-only. | Clear, reproducible leakage effect.
E03 | County data pilot | Coverage, suppression, crop-mask QA. | Enough counties/years for primary split.
E04 | Weather weighting ablation | Centroid vs crop-area weighted. | Validation improvement and stable external plan.
E05 | Phenology/drought/context ablation | Incremental value. | B1 improvement on development with uncertainty.
E06 | Model family grid | Pareto candidate. | Pass development Gate A/B1.
E07 | Uncertainty/conformal | Coverage and selective risk. | Valid coverage + improved abstention utility.
E08 | External county holdout | Final confirm. | Predefined external PASS.
E09 | Air-quality external domain | Generalization. | False-permission reduction or gate PASS/FAIL regimes.
E10 | Prototype triage | Workload/recall/trust. | Application value measurable.

## Table 31

Dimension | 0 | 1 | 2
Primary metric | Không improve | Point estimate improve, CI inconclusive | Pre-specified CI/significance PASS
Tail/application | At/below null | Một metric improve | Rank/recall@budget + uncertainty PASS
Robustness | Single split only | Mixed folds | Majority folds + external consistency
Novelty | Incremental implementation | Useful ablation | New benchmark/framework finding
Application | No user decision | Workflow stated | Measured triage/workload value
Reproducibility | Manual | Scripted | Clean clone + full traceability

## Table 32

Section | Nội dung
Introduction | Problem: unsafe weather narratives; users and triage decision.
Method | Selective-explanation gate + uncertainty + protocol.
Synthetic benchmark | Gate prevents false attribution under weak signal/leakage/drift.
Agriculture V2 | County-level, crop-weighted data and external holdout.
Results | Candidate model passes A/B1; application recall/workload.
Prototype | Analyst triage and abstention workflow.
Limitations | Not causal attribution; data availability; county aggregation.

## Table 33

Section | Nội dung
Introduction | XAI overclaim in temporal scientific ML.
Framework | Fidelity-gated selective explanation.
Synthetic benchmark | Main positive result: false-attribution reduction.
Crop case | Negative real-world case demonstrates abstention and data gaps.
External domain | Air-quality case demonstrates generality.
Application | Audit/triage tool that reports reason codes instead of causal narratives.

## Table 34

KHÔNG ĐƯỢC KITCHEN-SINK
Paper cuối chỉ giữ experiment phục vụ một luận điểm. Full logs và secondary ablations chuyển sang supplementary/repository. 8 trang phải ưu tiên method, key benchmark, applied case và application value.

## Table 35

Stage | Budget guidance
Pilot data | 1–3 states; one crop; small years; validate schemas.
CDL processing | Use state COG/windowed reads; avoid national 10m full downloads initially.
POWER | Deduplicate grid cells; cache; ≤5 workers.
Synthetic | Parallelize seeds; deterministic seed registry.
Model grid | Successive halving on development only; keep pre-specified max budget.
External | Single fixed run + uncertainty; no grid.

## Table 36

Sprint | Deliverables | Exit criterion
S0 — 1–2 ngày | Freeze baseline; prereg templates; source manifest; environment audit. | Reproduce baseline PASS.
S1 — 3–5 ngày | Synthetic DGP + ungated/ablation/full gate. | First false-attribution plots; no always-abstain.
S2 — 3–5 ngày | NASS county pilot + CDL + POWER + FIPS. | Pilot dataset QA PASS.
S3 — 5–10 ngày | Full Agriculture V2 build + context sources. | Development panel frozen.
S4 — 5–10 ngày | Model/target/uncertainty grid. | One development candidate or documented failure.
S5 — 2–4 ngày | External holdout one-shot. | external-confirmed or rejected tag.
S6 — 3–5 ngày | Air-quality domain if needed. | Generality result.
S7 — 3–5 ngày | Prototype and task evaluation. | Application metrics + screenshots.
S8 — 3–5 ngày | Paper integration, scorecard, repository release. | Paper candidate ≥80/100.

## Table 37

Source fact | Implication
NASA POWER Daily API supports JSON/CSV/NetCDF and data from 1981 to near real time. | Pin access date/data snapshot; rate-limit requests.
CDL has national coverage from 2008 onward; recent 2024–2025 releases include 10m and 30m products. | Primary annual crop-mask study should start 2008 unless using a separate historical design.
NASS Crop Progress gridded layers cover corn, soybeans, cotton and winter wheat from 2015 onward. | Use state weekly Quick Stats for longer stage history; gridded layers as sensitivity.
SoilGrids REST API may be paused/unreliable; WCS/WebDAV are recommended alternatives. | Do not design critical pipeline around REST endpoint.
USDM provides REST county/state weekly statistics and GIS data. | Build weekly drought exposure using FIPS and dates.
NASS Irrigation and Water Management is collected every five years. | Only use latest past survey for a year; no future interpolation.
EPA AirData offers pre-generated daily/hourly ZIP files and AQS API. | Good low-friction second-domain option.

## Table 38

KẾT LUẬN THỰC THI
Ưu tiên T1 synthetic benchmark, sau đó T2 county-level data và T5 analyst triage. Chỉ thêm model mà thiếu dữ liệu mới, external holdout và application evaluation sẽ không đủ đạt 8/10.
