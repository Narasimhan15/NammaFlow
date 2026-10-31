
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request

from nammaflow.data import load_data, build_summary


def as_records(frame):
    """Convert report rows to JSON-safe values, preserving missingness."""
    return json.loads(frame.to_json(orient="records"))


@asynccontextmanager
async def lifespan(app):
    profiles, suggestions = load_data()
    app.state.profiles = profiles
    app.state.suggestions = suggestions
    yield


app = FastAPI(
    title="Namma Yatri Flow API",
    description=(
        "Historical Bengaluru mobility analytics. "
        "Independent project using Namma Yatri data; "
        "not affiliated with or endorsed by Namma Yatri. "
        "Record geography is unverified. Investigation suggestions "
        "are exploratory, not confirmed causes or severity rankings. "
        "Summary rates are fractions; report fields retain source units."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health(request: Request):
    return {
        "status": "ok",
        "record_count": len(request.app.state.profiles),
    }


@app.get("/summary")
def summary(request: Request):
    return build_summary(
        request.app.state.profiles,
        request.app.state.suggestions,
    )


@app.get("/records")
def records(
    request: Request,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=250),
):
    profiles = request.app.state.profiles
    ordered = profiles.sort_values("ward_num")
    return {
        "total": len(ordered),
        "offset": offset,
        "limit": limit,
        "items": as_records(ordered.iloc[offset:offset + limit]),
    }


@app.get("/records/{record_id}")
def record_detail(record_id: str, request: Request):
    profiles = request.app.state.profiles
    matched = profiles[profiles["ward_num"].eq(record_id)]

    if matched.empty:
        raise HTTPException(status_code=404, detail="Record not found")

    suggestions = request.app.state.suggestions
    relevant = suggestions[suggestions["ward_num"].eq(record_id)]

    return {
        "profile": as_records(matched)[0],
        "suggestions": as_records(relevant),
    }


@app.get("/investigations")
def investigations(
    request: Request,
    record_id: str | None = None,
    rule_id: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=250),
):
    profiles = request.app.state.profiles
    suggestions = request.app.state.suggestions

    if record_id is not None:
        if not profiles["ward_num"].eq(record_id).any():
            raise HTTPException(status_code=404, detail="Record not found")
        suggestions = suggestions[
            suggestions["ward_num"].eq(record_id)
        ]

    if rule_id is not None:
        known_rules = request.app.state.suggestions["rule_id"]
        if not known_rules.eq(rule_id).any():
            raise HTTPException(status_code=404, detail="Rule not found")
        suggestions = suggestions[suggestions["rule_id"].eq(rule_id)]

    ordered = suggestions.sort_values(["ward_num", "rule_id"])
    return {
        "total": len(ordered),
        "offset": offset,
        "limit": limit,
        "items": as_records(ordered.iloc[offset:offset + limit]),
    }
