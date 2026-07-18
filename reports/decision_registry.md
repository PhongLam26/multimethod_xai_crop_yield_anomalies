# Decision Registry

- D-001: The DOCX plan is read-only and remains outside the repository. Status: ACCEPTED.
- D-002: No V2, synthetic, external-domain, or model experiments may run until Dataset V1 is frozen and verified. Status: ENFORCED.
- D-003: Dataset V1 remains the immutable state-level baseline; candidate work requires separate versioned artifacts. Status: ACCEPTED.
- D-004: V2 population is the pre-model locked `WHEAT__WINTER` county panel chosen solely by canonical source-coverage rules. The 2022-2025 temporal holdout may not be used for model or feature-family selection. Status: ENFORCED.
- D-005: V2's selected weather-only model has a Gate A confidence interval crossing zero; its required action is `ABSTAIN`, not an agricultural predictive or weather-specific explanation claim. Status: ENFORCED.
