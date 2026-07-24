# Reference Forensic Audit

Checked: 2026-07-18

Scope: the 19 references emitted by `paper/ictai2026_blind/main.bbl`.  The final
PDF has no uncited bibliography entries because IEEE BibTeX emits only cited keys.

| Citation group | Keys | Metadata check | Result |
|---|---|---|---|
| Crop-yield forecasting | Paudel2021, Meroni2021, Khaki2019, LengHall2020 | Title, author list, journal, year, and DOI checked against publisher/index records | PASS |
| Weather extremes and yield | Lesk2016, Zampieri2017, Vogel2019, Heino2023, Schierhorn2021, Sjulgard2023 | Title, venue, year, volume/article number, and DOI checked; corrected `Matias Heino`, `Max Hofmann`, and diacritics in the BibTeX record | PASS |
| Detrending literature | Ray2015, Lu2017, Meng2024 | Title, venue, year, pages/article number, and DOI checked | PASS |
| XAI methods | LundbergLee2017, Ribeiro2016, Fisher2019, ApleyZhu2020 | Venue/year and persistent identifier or official proceedings/JMLR record checked | PASS |
| Data sources | USDANASSQuickStats, NASAPOWER2025 | Official USDA NASS and NASA POWER documentation checked; access date remains explicitly recorded | PASS |

Representative primary records used for the check: Paudel et al. DOI
`10.1016/j.agsy.2020.103016`; Zampieri et al. DOI
`10.1088/1748-9326/aa723b`; Schierhorn et al. DOI
`10.1007/s10584-021-03272-0`; Apley and Zhu DOI `10.1111/rssb.12377`; and the
official USDA NASS Quick Stats and NASA POWER API documentation.

The literature is used for background and method descriptions only.  It is not used
to justify a causal weather-driver conclusion from this study's residual model.
