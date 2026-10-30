# Decision & Recommendation Reports

- investigation_suggestions.csv: one row per record–rule trigger.
- record_review.csv: all input profiles plus trigger counts.
- threshold_sensitivity.csv: one-at-a-time threshold comparisons.
- metadata.json: rules, configuration, provenance and file hashes.

Rates are fractions; missing values remain blank.

## Limitations

- Exploratory configurable thresholds; human review required.
- Threshold sensitivity does not establish accuracy.
- All geographic mappings remain unverified.
- Supply timing compatibility remains unresolved.
- No causal, driver-shortage, uplift or operational-priority claims.
- Clusters and anomaly scores provide context only.
- No triggered rule does not establish that a record has no issues.
