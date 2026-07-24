"""Write a source-backed support matrix for the methodological references."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "audit" / "references" / "methodology_reference_support.csv"


ROWS = [
    {
        "key": "ElYanivWiener2010",
        "method_area": "selective classification / reject option",
        "supports_claim": "abstention trades coverage for risk and motivates explicit permission/abstain reporting",
        "primary_source": "https://jmlr.org/papers/v11/el-yaniv10a.html",
        "source_type": "JMLR article page",
        "manuscript_location": "Related Work / Selective Prediction and Abstention",
        "status": "VERIFIED",
    },
    {
        "key": "GeifmanElYaniv2017",
        "method_area": "selective classification / risk coverage",
        "supports_claim": "risk-controlled rejection motivates reporting coverage, risk, and false abstention trade-offs",
        "primary_source": "https://papers.neurips.cc/paper/7073-selective-classification-for-deep-neural-networks",
        "source_type": "NeurIPS proceedings page",
        "manuscript_location": "Related Work / Selective Prediction and Abstention",
        "status": "VERIFIED",
    },
    {
        "key": "Janzing2020",
        "method_area": "feature relevance and causal boundary",
        "supports_claim": "feature relevance requires explicit estimand/reference distribution and is not automatically causal",
        "primary_source": "https://proceedings.mlr.press/v108/janzing20a.html",
        "source_type": "PMLR proceedings page",
        "manuscript_location": "Related Work / Explanation Methods and Their Boundary",
        "status": "VERIFIED",
    },
    {
        "key": "Slack2020",
        "method_area": "post-hoc explanation reliability",
        "supports_claim": "perturbation-based post-hoc explanations can be unreliable under adversarial/OOD behavior",
        "primary_source": "https://dl.acm.org/doi/10.1145/3375627.3375830",
        "source_type": "ACM DOI page",
        "manuscript_location": "Related Work / Explanation Methods and Their Boundary",
        "status": "VERIFIED",
    },
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ROWS[0].keys())
        writer.writeheader()
        writer.writerows(ROWS)
    print(f"Wrote {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
