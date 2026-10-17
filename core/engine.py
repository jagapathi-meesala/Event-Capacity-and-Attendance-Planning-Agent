"""Transparent event attendance and venue capacity calculations."""

def validate_event_plan(payload):
    issues = []
    if not isinstance(payload, dict):
        return [{"path": "$", "message": "Input must be a JSON object."}]
    event = payload.get("event")
    if not isinstance(event, dict):
        return [{"path": "$.event", "message": "Required event object is missing."}]
    name = event.get("name")
    if not isinstance(name, str) or not name.strip():
        issues.append({"path": "$.event.name", "message": "Event name is required."})
    registrations = event.get("registrations")
    if not isinstance(registrations, int) or isinstance(registrations, bool) or registrations < 0:
        issues.append({"path": "$.event.registrations", "message": "Registrations must be a non-negative integer."})
    rsvp_rate = event.get("expected_attendance_rate")
    if not isinstance(rsvp_rate, (int, float)) or isinstance(rsvp_rate, bool) or not 0 <= rsvp_rate <= 1:
        issues.append({"path": "$.event.expected_attendance_rate", "message": "Expected attendance rate must be between 0 and 1."})
    venue = payload.get("venue")
    if not isinstance(venue, dict):
        issues.append({"path": "$.venue", "message": "Required venue object is missing."})
    else:
        capacity = venue.get("approved_capacity")
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            issues.append({"path": "$.venue.approved_capacity", "message": "Approved capacity must be a positive integer."})
    return issues

def estimate_attendance(payload):
    issues = validate_event_plan(payload)
    if issues:
        return {"status": "needs_input_correction", "validation_issues": issues, "estimate": None}
    event = payload["event"]
    venue = payload["venue"]
    registrations = event["registrations"]
    rate = event["expected_attendance_rate"]
    estimate = round(registrations * rate)
    capacity = venue["approved_capacity"]
    difference = estimate - capacity
    if estimate > capacity:
        status = "capacity_exceeded"
        warning = "Estimated attendance exceeds the supplied approved venue capacity. Review registrations, venue capacity, and safety arrangements with the venue organizer."
    elif estimate == capacity:
        status = "at_capacity"
        warning = "Estimated attendance equals the supplied approved venue capacity; confirm operating arrangements with the venue."
    else:
        status = "within_capacity"
        warning = "Estimate is below the supplied capacity, but this is not a safety or legal compliance determination."
    return {
        "status": status,
        "event": {"name": event["name"], "registrations": registrations},
        "venue": {"name": venue.get("name"), "approved_capacity": capacity},
        "attendance_estimate": estimate,
        "expected_attendance_rate": rate,
        "calculation": f"round({registrations} registrations × {rate} attendance rate) = {estimate}",
        "capacity_difference": difference,
        "estimated_capacity_utilization": round(estimate / capacity, 4),
        "assumptions": [
            "The attendance rate is supplied by the organizer and is not independently verified.",
            "The estimate is a planning estimate, not a guaranteed headcount.",
            "Approved capacity is taken from supplied input and must be verified with the venue."
        ],
        "warnings": [warning, "Confirm emergency exits, accessibility, staffing, and applicable venue rules with responsible personnel."],
        "human_review_required": True,
        "validation_issues": []
    }

def generate_report(payload):
    report = estimate_attendance(payload)
    report["report_type"] = "event_capacity_attendance_plan"
    report["agent"] = "event-capacity-attendance-planning-agent"
    return report
