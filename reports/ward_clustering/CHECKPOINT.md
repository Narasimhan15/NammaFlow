# Ward clustering — reviewed exploratory checkpoint

Updated 26 October 2026. Notebook 05 covers the clustering component of project roadmap Phase 6, Unsupervised Learning & Anomaly Detection. Anomaly detection remains outstanding.

## Scope and findings

241 eligible records; three zero-booking records with undefined completion rates excluded from fitting and retained separately. Inputs: log1p(searches), booking conversion and booking completion, standardized before clustering. Driver supply is excluded because temporal compatibility is unverified; w_0 geography remains unresolved.

K-Means k=4 silhouette: 0.3000; cluster sizes: 71, 46, 69, 55. Ward hierarchical k=4 silhouette: 0.2588; cluster sizes: 91, 55, 41, 54. Between-method ARI: 0.5588. Broad profiles recur, but memberships differ.

The exploratory >=10-bookings scenario retains 174 records and excludes 67. K-Means ARI against the original grouping: 0.3408 with original scaling and 0.2777 with refitted scaling. Ward ARI: 0.3474 with original scaling and 0.1821 with refitted scaling. Ward silhouettes in these scenarios: 0.2755 and 0.2453 respectively.

Decision: retain K-Means k=4 as an exploratory description of this dataset. Robust operational ward categories have not been established. Cluster assignments alone should not prescribe interventions.

## Review and validation

All nonempty notebook code cells parse; no saved error outputs. New comparison and export cells have execution counts 17–21. Earlier cells retain saved outputs but blank execution counts in this export; prior session screenshots support their execution. This review did not execute the notebook end to end or deserialize the joblib model. The saved reload assertion reports matching assignments.

ZIP integrity, 241 unique assignment IDs, disjoint excluded IDs, cluster counts, and agreement of raw features and K-Means labels between assignment CSVs were checked. Comparison CSVs match supplied notebook outputs.

Publication edits clarify roadmap numbering, remove an empty cell and the redundant standalone reload check already included in 5.6.1. The optional Colab ZIP-download cell remains at the end.

## Outstanding project work

Review anomaly-detection scope, demand–supply temporal compatibility and geographic mapping against the ten-phase roadmap. The latest supervised-learning summary and dependency versions still require separate repository review.

No GitHub commit or push was made by this review.
