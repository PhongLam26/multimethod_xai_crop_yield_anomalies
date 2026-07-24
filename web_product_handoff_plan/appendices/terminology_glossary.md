# Terminology Glossary

| Term | Definition |
|---|---|
| Locked target | Observed outcome vector reserved for evaluation, not model selection. |
| Row ID | Stable identifier used to pair target and prediction vectors. |
| Block ID | Cluster or temporal unit used for paired bootstrap resampling. |
| Selected prediction | Prediction from the prespecified selected model or method. |
| Baseline prediction | Prespecified comparison vector for overall adequacy. |
| Full prediction | Prediction using feature family plus allowed context. |
| Restricted prediction | Prediction excluding the requested feature family. |
| Feature family | Domain-configurable group of predictors, such as weather or forecast. |
| Module A | Overall predictive adequacy check. |
| Module B | Incremental feature-family value check. |
| Module E | Event recovery check for requested event-level claims. |
| Module D | Diagnostic-only module outside the permission path. |
| Claim hierarchy | Deterministic mapping from module outcomes to highest permitted interpretation. |
| False permission | Policy permits a claim that evaluation labels mark invalid in a benchmark. |
| False abstention | Policy abstains from a claim that evaluation labels mark valid in a benchmark. |
| GT labels | Ground-truth benchmark labels used only for evaluation. |

