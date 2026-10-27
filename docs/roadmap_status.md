# NammaFlow — Roadmap status checkpoint

28 October 2026. Based on reviewed local notebooks, exported reports, saved Colab outputs, and user-reported commits. This is not verification of the current GitHub head.

Notebook numbers and original roadmap phase numbers differ. Keep notebook section numbers stable; clarify roadmap phase in introductory text.

| Original phase | Current evidence and status |
|---|---|
| 1. Data Understanding & Structural Cleaning | Notebook 01 exists; not re-audited in this checkpoint. |
| 2. Exploratory Data Analysis | Notebook 02 contains temporal, category, funnel, ward, and driver analyses; earlier operational claims require review against timing limitations. |
| 3. Feature Engineering | Notebook 03 builds ward intelligence and cross-domain features; source timing compatibility remains unresolved. |
| 4. Demand–Supply Intelligence | Addressed across notebooks 02–03, not a missing standalone notebook. Descriptive work exists; compatible observation windows and operational interpretation are unverified. |
| 5. Supervised Machine Learning | Notebook 04 contains baselines, CV, nested CV, explainability and evaluation. Historical conversion model remains provisional. Latest Colab/GitHub summary synchronization and dependency documentation need verification. |
| 6. Unsupervised Learning & Anomaly Detection | Planned exploratory scope implemented in notebooks 05–06, with sensitivity analyses and exports reviewed. User reports commits completed. No labelled anomaly accuracy or operational segmentation established. |
| 7. Spatial / Ward-Level Intelligence | Notebook 07 joins 244 profiles, preserves three exclusions, and exports comparisons. Spatial component pending verified identifier lookup and compatible boundary data. User reports commit completed. |
| 8. Decision & Recommendation Engine | Not implemented in this session. Define transparent investigation rules and evidence before implementation. |
| 9. Dashboard + API / NammaFlow Application | Not verified as implemented; existing local folder names alone do not establish working functionality. |
| 10. Deployment, Documentation & Portfolio Packaging | Pending final implementation, environment validation and presentation. |

## Immediate closeout work

1. Obtain the latest Colab notebook 04 and compare its final evaluation summary with the intended repository version. Local copies differ (184 versus 280 cells); do not overwrite based solely on filename or cell count.
2. Document working dependency versions. Local requirements.txt is empty. Anomaly metadata records sklearn 1.6.1, numpy 2.1.3, pandas 2.2.3 and joblib 1.6.0; this does not establish a complete environment for SHAP or the application.
3. Carry explicit supply timing and geography limitations into the project README and later decision rules. These external data gaps need not prevent a constrained investigation workflow.
4. Define Phase 8 acceptance criteria: reproducible rules, counts and evidence displayed, missing data handled, w_0 flagged, no causal or shortage claims from unverified supply comparisons, and no invented prediction accuracy or estimated operational uplift.

## Model interpretation

Recorded ordinary MAE: Random Forest 9.0341 percentage points versus baseline 8.4156. Demand-weighted MAE: 4.3796 versus approximately 6.69 percentage points. Improvements differ by demand segment. Earlier holdout inspection limits independence; future-period forecasting is not established.

## Review boundary

Recent notebook and CSV reviews checked code syntax, saved execution/error state, identifier coverage, calculations and exported consistency. They did not independently rerun all historical notebooks end to end or verify live GitHub commits.
