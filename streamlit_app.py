import pandas as pd
import streamlit as st
from nammaflow.data import load_data, build_summary

st.set_page_config(page_title="Namma Yatri Flow", layout="wide")

st.title("Namma Yatri Flow")
st.caption("Bengaluru Mobility Analytics")
st.caption("Independent analytics project using Namma Yatri data. Not affiliated with or endorsed by Namma Yatri.")

try:
    profiles, suggestions = load_data()
except (OSError, ValueError) as exc:
    st.error(f"Unable to load validated reports: {exc}")
    st.stop()

st.warning(
    "Area names use Namma Yatri’s published dashboard lookup. "
    "Map boundaries and historical boundary compatibility remain unverified. "
    "Suggestions support investigation; they do not establish causes "
    "or operational priorities."
)

unmapped = profiles["ward_name_status"].eq("unmapped")
if unmapped.any():
    st.warning(f"{int(unmapped.sum())} records have no publisher name; shown as Unknown area with their original ID.")
st.caption("Name source: [Namma Yatri official dashboard](https://nammayatri.in/open/), retrieved 12 November 2026.")

overview, records, investigations = st.tabs(
    ["Overview", "Record explorer", "Investigation explorer"]
)

def percentage(value):
    return "Unavailable" if value is None or pd.isna(value) else f"{value:.2%}"

with overview:
    summary = build_summary(profiles, suggestions)
    st.caption("Includes all records, including Other Wards (w_0).")

    columns = st.columns(4)
    for column, label, key in zip(
        columns,
        ["Records", "Searches", "Bookings", "Completed rides"],
        ["record_count", "searches", "bookings", "completed_rides"],
    ):
        column.metric(label, f"{summary[key]:,}")

    columns = st.columns(3)
    for column, label, key in zip(
        columns,
        ["Search to booking", "Booking completion", "Search to completion"],
        ["search_to_booking_rate", "booking_completion_rate",
         "search_to_completion_rate"],
    ):
        column.metric(label, percentage(summary[key]))

    st.caption("Aggregate rates use summed counts, not averages of record rates.")
    st.subheader("Investigation coverage")
    st.write(
        f"{summary['suggestion_count']} suggestions across "
        f"{summary['records_with_suggestions']} records."
    )
    st.dataframe(
        suggestions.groupby("rule_id").size().rename("Suggestion count"),
        width="stretch",
    )

with records:
    labels = profiles.set_index("ward_num")["display_name"].to_dict()
    selected = st.selectbox(
        "Area / ward", sorted(labels, key=lambda key: (labels[key].casefold(), key)),
        format_func=labels.get
    )
    record = profiles.loc[profiles["ward_num"] == selected]
    row = record.iloc[0]
    st.subheader(row["display_name"])

    columns = st.columns(3)
    columns[0].metric("Searches", f"{int(row['ward_searches']):,}")
    columns[1].metric("Bookings", f"{int(row['ward_bookings']):,}")
    columns[2].metric("Completed rides", f"{int(row['ward_completed_rides']):,}")

    st.write("Search to booking:", percentage(row["ward_search_to_booking_rate"]))
    st.write("Booking completion:", percentage(row["ward_booking_completion_rate"]))

    if row["ward_bookings"] == 0:
        st.info("No bookings: booking completion rate is undefined.")
    if selected == "w_0":
        st.info("Namma Yatri labels w_0 as Other Wards. Its exact coverage is unspecified; it is not a single mapped ward.")

    st.subheader("Exploratory model context")
    st.caption(
        "Clusters describe exploratory groupings. Higher anomaly scores mean "
        "more unusual patterns, not greater severity. Missing values are unavailable."
    )
    context = [
        "has_model_results", "exclusion_reason", "exploratory_cluster",
        "anomaly_score",
    ]
    st.dataframe(record[context], hide_index=True, width="stretch")

    st.subheader("Suggestions for this record")
    matching = suggestions.loc[suggestions["ward_num"] == selected]
    if matching.empty:
        st.info("No rules triggered. This does not establish that no issues exist.")
    else:
        st.dataframe(
            matching[["ward_name", "ward_num", "rule_id", "suggested_investigation", "limitations"]],
            hide_index=True, width="stretch",
        )

    with st.expander("All profile fields — raw rates are fractions"):
        st.caption("geographic_mapping_status is the original report assessment. ward_name_status describes the newly added publisher label; boundaries remain unverified.")
        st.dataframe(
            record.T.rename(columns={record.index[0]: "Value"}).astype("string"),
            width="stretch",
        )

with investigations:
    rule = st.selectbox(
        "Rule", ["All"] + sorted(suggestions["rule_id"].unique().tolist())
    )
    filtered = suggestions if rule == "All" else suggestions[
        suggestions["rule_id"] == rule
    ]
    st.write(
        f"{len(filtered)} suggestions across "
        f"{filtered['ward_num'].nunique()} records."
    )
    st.caption("Raw rates are fractions. Missing values are unavailable. Original investigation text is retained; geographic caveats predate the added publisher names.")
    st.dataframe(filtered, hide_index=True, width="stretch")

with st.expander("Data and interpretation limitations"):
    st.markdown(
        "- Historical reports do not establish forecasting accuracy.\n"
        "- Names come from Namma Yatri’s current dashboard lookup, retrieved 12 November 2026.\n"
        "- Names do not certify current legal wards or historical boundary compatibility; maps are deferred.\n"
        "- Original report geography fields and investigation text retain their historical assessment.\n"
        "- Supply timing compatibility remains unverified.\n"
        "- Rule thresholds are exploratory and sensitive to configuration.\n"
        "- Low booking counts can produce unstable rates.\n"
        "- Missing model outputs and undefined rates remain unavailable."
    )
