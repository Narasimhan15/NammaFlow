import sys
import importlib
import math

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
importlib.invalidate_caches()

import api
api = importlib.reload(api)

from fastapi.testclient import TestClient

with TestClient(api.app) as client:
    def get_ok(path, **params):
        response = client.get(path, params=params)
        assert response.status_code == 200, response.text
        return response.json()

    # Startup and aggregate totals
    health = get_ok("/health")
    assert health == {"status": "ok", "record_count": 244}

    summary = get_ok("/summary")
    expected = {
        "record_count": 244,
        "searches": 36112,
        "bookings": 9936,
        "completed_rides": 4778,
        "suggestion_count": 149,
        "records_with_suggestions": 147,
        "suggestions_by_rule": {
            "R01": 2, "R02": 76, "R03": 70, "R04": 1
        },
    }
    for key, value in expected.items():
        assert summary[key] == value, (key, summary[key])

    for key, numerator, denominator in [
        ("search_to_booking_rate", 9936, 36112),
        ("booking_completion_rate", 4778, 9936),
        ("search_to_completion_rate", 4778, 36112),
    ]:
        assert math.isclose(
            summary[key], numerator / denominator, rel_tol=1e-12
        )

    print("✅ Health, totals, and aggregate rates")

    # Pagination must preserve every record exactly once
    rows = []
    for offset in range(0, 244, 50):
        page = get_ok("/records", offset=offset, limit=50)
        assert page["total"] == 244
        rows.extend(page["items"])

    ids = [row["ward_num"] for row in rows]
    assert len(ids) == len(set(ids)) == 244
    assert "w_0" in ids
    assert get_ok("/records", offset=244)["items"] == []

    # Every record detail must agree with its list entry
    for row in rows:
        detail = get_ok(f"/records/{row['ward_num']}")
        assert detail["profile"] == row
        assert all(
            item["ward_num"] == row["ward_num"]
            for item in detail["suggestions"]
        )

    print("✅ Pagination and all 244 record details")

    # Zero bookings must retain an undefined completion rate
    for record_id in ["b_168", "b_26", "b_44"]:
        profile = get_ok(f"/records/{record_id}")["profile"]
        assert profile["ward_bookings"] == 0
        assert profile["ward_booking_completion_rate"] is None
        assert profile["has_model_results"] is False

    profile = get_ok("/records/b_168")["profile"]
    assert profile["ward_searches"] == 13
    assert profile["ward_completed_rides"] == 0

    print("✅ Zero-booking records preserve JSON null")

    # Investigation filters and valid empty results
    all_suggestions = get_ok("/investigations", limit=250)
    assert all_suggestions["total"] == 149
    assert len(all_suggestions["items"]) == 149

    r01 = get_ok("/investigations", rule_id="R01")
    assert r01["total"] == 2
    assert {x["ward_num"] for x in r01["items"]} == {
        "b_131", "b_181"
    }

    combined = get_ok(
        "/investigations", record_id="b_181", rule_id="R01"
    )
    assert combined["total"] == 1
    assert combined["items"][0]["ward_num"] == "b_181"
    assert combined["items"][0]["rule_id"] == "R01"

    empty = get_ok("/investigations", record_id="b_1")
    assert empty["total"] == 0
    assert empty["items"] == []

    print("✅ Investigation filters and valid empty results")

    # Unknown identifiers and invalid pagination
    for path, params, status in [
        ("/records/unknown_record", {}, 404),
        ("/investigations", {"record_id": "unknown_record"}, 404),
        ("/investigations", {"rule_id": "unknown_rule"}, 404),
        ("/records", {"offset": -1}, 422),
        ("/records", {"limit": 0}, 422),
        ("/records", {"limit": 251}, 422),
        ("/investigations", {"offset": -1}, 422),
        ("/investigations", {"limit": 0}, 422),
        ("/investigations", {"limit": 251}, 422),
    ]:
        response = client.get(path, params=params)
        assert response.status_code == status, (
            path, params, response.status_code, response.text
        )

    print("✅ Unknown identifiers and invalid pagination")

print("\n✅ API integration checks passed.")