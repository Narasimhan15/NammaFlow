# Publisher ward names — 12 November 2026

The application now adds readable area names to profiles and investigation suggestions. For example, `b_181` displays as **Shantala Nagar (b_181)**, `b_168` as **Padarayanapura (b_168)**, `b_186` as **Koramangala (b_186)**, and `w_0` as **Other Wards (w_0)**.

## Provenance and scope

Source page: https://nammayatri.in/open/

Its HomeRoute.bs.a335ce8b.js bundle imports https://nammayatri.in/chunks/HomeLayout.bs.aa195fb1.js, whose `getBangaloreWardName` function supplies 244 explicit names. The source URL, retrieval date and SHA-256 are recorded in `data/reference/ward_names.json`. All 244 project profile IDs match. Names retain the publisher's spelling.

These are labels from the current publisher dashboard, not certification of present legal ward boundaries or unchanged geography since the original data download. SVG shapes found in the website are not yet validated as geographic coordinates. Maps remain deferred. “Other Wards” is a publisher catch-all label, not a verified single ward; its exact coverage remains unspecified.

## Application and API

The shared loader adds `ward_name`, `display_name` and `ward_name_status` to profiles and suggestions. Names are resolved at load time without editing the historical CSV reports or recalculating rules. Existing API routes, record IDs, filtering, pagination and summary values remain unchanged. Clients of `/records`, `/records/{record_id}` and `/investigations` receive these additive fields. API version: 0.2.0.

The original `geographic_mapping_status` and investigation wording remain historical source content. The new `ward_name_status=publisher_label_verified` describes only name verification. Unknown IDs keep their records and counts, receive a null name, `unmapped` status and an `Unknown area (ID)` display label. Duplicate lookup keys and invalid names are rejected.

## Validation

Run from the repository root using the application's installed dependencies:

```sh
python tests/check_api.py
python tests/check_geography.py
```

Passed locally against GitHub base commit `2057cea31f9fc71146be5f895eca5dd093622434`:
- Existing API integration checks, including all 244 detail responses, null rates, filters and pagination.
- Exact equality of every original profile and suggestion field before/after enrichment.
- Publisher names across records and investigation API responses.
- Missing lookup entry preservation and duplicate-key rejection.
- Streamlit selection for the four example IDs and R01 filtering.
- Updated notebook generation matches the application code; notebook dashboard checks pass, including all four rules.

The entire historical analysis pipeline was not rerun. Notebook outputs were cleared to avoid displaying stale execution evidence. Non-failing warnings concern Starlette's HTTPX deprecation and Streamlit's test context.

## GitHub upload

Upload the contents of the accompanying update folder at the repository root, merging folders and replacing the listed files. Do not upload the ZIP itself as source. The update contains only changed/new files and needs the existing repository reports and requirements.

After deploying, check the record selector for Shantala Nagar, Padarayanapura, Koramangala and Other Wards; confirm Padarayanapura retains unavailable booking completion and R01 still contains two records. No remote commit or deployment was performed during local validation.
