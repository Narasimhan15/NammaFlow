# Evaluation checkpoint — 26 October 2026

Verified exported CSV consistency: 49 unique test wards; 8,138 searches; demand-weighted MAE 4.3796 pp; 16 wards above 10 pp absolute error; maximum 30.55 pp.

Random Forest weighted MAE versus training-mean baseline: low demand 15.2567 vs 13.0091 pp; medium 5.6373 vs 5.0695 pp; high 3.8160 vs 6.6437 pp. High-demand wards represent 86.38% of test searches. Ordinary MAE previously recorded in the notebook: Random Forest 9.0341 pp versus baseline 8.4156 pp. The model is provisional and estimates historical ward booking conversion; temporal generalization has not been established.

## Package changes
- Latest notebook analysis and available outputs retained; removed obsolete Git upload, duplicate cleanup, identity, authentication and commit/push cells (original zero-based indices 180–192), plus the temporary ZIP download cell and trailing empty cells.
- Removed 0 stored error outputs. Original user downloads remain unchanged.
- Included recovery notebook, three CSVs and available demand-segment figure.
- Model artifacts and metadata remain unchanged.

## Validation and remaining work
CSV aggregates were independently recomputed from the exported ward table. Notebook JSON is readable and common GitHub/OpenAI token patterns were scanned. Notebooks were not executed end to end; absence of matching token patterns is not a complete secret audit. Recovery has already been demonstrated by the user's Colab screenshots.
The repository requirements.txt is empty. Dependency pinning still needs the working Colab versions, including SHAP. Saved model metadata records scikit-learn 1.6.1.

## Apply to GitHub
Copy package paths into the repository, preserving folders. Review the notebook and diff, then commit the notebook files and reports/model_evaluation directory. Suggested commit: Save model explainability and evaluation checkpoint.
No commit or push has been performed by Codex. This package contains replacements/additions only; do not replace the whole repository with it.
