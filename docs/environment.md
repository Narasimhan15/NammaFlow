# Analysis environment

Captured from the user-provided Colab version output on 28 October 2026.
Python: 3.13.18. Direct package versions are recorded in requirements.txt.

This records the current environment. Continuity with the historical ML/SHAP
runtime is unconfirmed. Version availability does not establish successful
imports, fresh installation, model loading, or end-to-end notebook execution.
The file is not a complete transitive dependency lock or application/API environment.
Google Colab supplies notebook-specific modules such as google.colab.

The anomaly checkpoint independently records matching numpy, pandas,
scikit-learn and joblib versions. Historical model artifacts should be used
with their recorded software metadata. SHAP compatibility still requires
execution validation; no historic SHAP version was established by this audit.

Next reproducibility check: use a separate clean environment, install the
recorded analysis dependencies, execute notebooks in their documented order,
and compare key outputs. Avoid using repeated holdout inspection to tune models.
