from pathlib import Path
import pandas as pd

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

PROFILE_COLUMNS = [
    "ward_num", "ward_searches", "ward_bookings",
    "ward_completed_rides", "ward_search_to_booking_rate",
    "ward_booking_completion_rate", "has_model_results",
    "exclusion_reason", "exploratory_cluster", "anomaly_score",
    "geographic_mapping_status",
]

SUGGESTION_COLUMNS = [
    "ward_num", "rule_id", "suggested_investigation", "limitations",
]


def load_data(root=None):
    """Load reports without replacing missing values or excluding records."""
    root = Path(root) if root is not None else DEFAULT_ROOT

    profiles = pd.read_csv(
        root / "reports/ward_level_intelligence/ward_profiles.csv",
        dtype={"ward_num": "string"},
    )
    suggestions = pd.read_csv(
        root / "reports/decision_recommendation/investigation_suggestions.csv",
        dtype={"ward_num": "string", "rule_id": "string"},
    )

    for name, frame, required in [
        ("profiles", profiles, PROFILE_COLUMNS),
        ("suggestions", suggestions, SUGGESTION_COLUMNS),
    ]:
        missing = sorted(set(required) - set(frame.columns))
        if missing:
            raise ValueError(f"{name}: missing columns {missing}")

    if profiles.empty:
        raise ValueError("Profiles report is empty.")

    for name, frame in [("profiles", profiles), ("suggestions", suggestions)]:
        ids = frame["ward_num"]
        if ids.isna().any() or ids.str.strip().eq("").any():
            raise ValueError(f"{name}: missing or blank record identifiers.")

    if profiles["ward_num"].duplicated().any():
        raise ValueError("Profiles contain duplicate record identifiers.")

    if suggestions["rule_id"].isna().any():
        raise ValueError("Suggestions contain missing rule identifiers.")

    if suggestions.duplicated(["ward_num", "rule_id"]).any():
        raise ValueError("Duplicate record-rule suggestions found.")

    if not suggestions["ward_num"].isin(profiles["ward_num"]).all():
        raise ValueError("Suggestions reference unknown records.")

    counts = ["ward_searches", "ward_bookings", "ward_completed_rides"]
    for column in counts:
        values = pd.to_numeric(profiles[column], errors="raise")
        if (
            values.isna().any()
            or not values.between(0, float("inf"), inclusive="left").all()
            or values.mod(1).ne(0).any()
        ):
            raise ValueError(f"{column}: expected finite nonnegative counts.")

    return profiles, suggestions

# --- Summary functions ---

def build_summary(profiles, suggestions):
    """Summarize the supplied records and their matching suggestions."""
    relevant = suggestions[
        suggestions["ward_num"].isin(profiles["ward_num"])
    ]

    searches = int(profiles["ward_searches"].sum())
    bookings = int(profiles["ward_bookings"].sum())
    completed = int(profiles["ward_completed_rides"].sum())

    def safe_rate(numerator, denominator):
        return numerator / denominator if denominator else None

    return {
        "record_count": int(len(profiles)),
        "searches": searches,
        "bookings": bookings,
        "completed_rides": completed,
        "search_to_booking_rate": safe_rate(bookings, searches),
        "booking_completion_rate": safe_rate(completed, bookings),
        "search_to_completion_rate": safe_rate(completed, searches),
        "suggestion_count": int(len(relevant)),
        "records_with_suggestions": int(relevant["ward_num"].nunique()),
        "suggestions_by_rule": {
            str(rule): int(count)
            for rule, count in relevant.groupby("rule_id").size().items()
        },
    }
