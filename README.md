# Event Capacity and Attendance Planning Agent

A deterministic planning assistant that validates event planning inputs, estimates attendance from supplied registration and response assumptions, checks estimates against stated venue capacity, and produces a traceable JSON report.

## Features
- Validates event, registration, RSVP, and venue-capacity fields.
- Calculates a transparent attendance estimate from supplied inputs.
- Compares expected attendance with stated venue capacity.
- Shows assumptions, calculation steps, and uncertainty warnings.
- Flags plans that need organizer or venue-safety review.

## Important limitations
This agent does not verify real-world registrations, venue certificates, fire codes, accessibility, evacuation plans, or local legal requirements. Estimates depend on supplied assumptions and are not guarantees. The venue's legally approved capacity and safety instructions take precedence. Do not use this tool alone to make safety-critical decisions.

## Requirements
Python 3.10+; no third-party dependencies.

## Run
```bash
python3 verification/readiness_audit.py
python3 -m unittest discover -s tests -v
python3 -m core.cli examples/event_plan.json --output event_report.json
```
