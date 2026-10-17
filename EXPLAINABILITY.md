# Explainability and Decision Transparency

## Purpose
The Event Capacity and Attendance Planning Agent validates supplied event planning data, estimates likely attendance using an organizer-provided attendance rate, and compares that estimate with a supplied approved venue capacity. It supports planning; it does not certify safety.

## Inputs
The JSON input contains an `event` object with `name`, non-negative integer `registrations`, and `expected_attendance_rate` from 0 to 1, plus a `venue` object with a positive integer `approved_capacity`. Optional names and dates are carried as descriptive context. The agent does not verify registrations or venue records externally.

## Decision
The agent validates required fields, calculates the estimate as `round(registrations × expected_attendance_rate)`, and compares the result with the supplied capacity. The estimate and all assumptions are included in the report. It does not silently change the inputs.

## Attendance Estimation
The estimate is a simple arithmetic projection based on the rate provided by the organizer. It is not learned from historical attendance data, does not account for uncertainty distributions, and is not a guaranteed count.

## Capacity Assessment
If the estimate exceeds capacity, the status is `capacity_exceeded`; if equal, `at_capacity`; otherwise `within_capacity`. Every result requires human review. Capacity is taken from the supplied input and must be verified against the venue's current approved limit.

## Outputs and Evidence
The report includes registration count, attendance rate, calculation, estimated headcount, approved capacity, capacity difference, utilization, assumptions, warnings, and validation issues. Values are traceable to supplied inputs and deterministic arithmetic.

## Tool: validate-event-plan

### Inputs and Data Sources
Receives the supplied event and venue JSON objects. No external registration system or venue database is queried.

### Decision and Reasoning
Checks event and venue object shapes, event name, non-negative integer registrations, attendance rate between zero and one, and positive integer approved capacity.

### Outputs and Evidence
Returns validation issues with paths and explanations. Valid input means only that the supplied fields pass these structural checks.

### Limits and Constraints
The tool cannot confirm that registrations, attendance rate, or approved capacity are accurate.

### Failure Handling
Invalid or missing fields are returned as validation issues; the tool does not invent replacement values.

### Human Review
The organizer should correct input errors and confirm the venue capacity and attendance assumptions.

## Tool: estimate-attendance

### Inputs and Data Sources
Receives validated registration count, attendance rate, and venue capacity from the input payload.

### Decision and Reasoning
Computes the rounded product of registrations and the supplied attendance rate, then compares the estimate with capacity.

### Outputs and Evidence
Returns the estimate, formula, capacity difference, utilization, status, assumptions, and warnings.

### Limits and Constraints
The estimate does not account for unregistered guests, staff, vendors, or changes in attendance unless those are included in the supplied planning inputs.

### Failure Handling
If input validation fails, no attendance estimate is produced. Capacity exceedance is flagged rather than concealed.

### Human Review
An organizer must consider staff, vendors, walk-ins, and other occupants when applicable and should not use the estimate to override venue limits.

## Tool: generate-capacity-report

### Inputs and Data Sources
Receives the validation and calculation result from the other tools.

### Decision and Reasoning
Packages the calculations and warnings into a structured report without making new claims about real-world conditions.

### Outputs and Evidence
Produces a JSON report for event planning and review.

### Limits and Constraints
A report is not a crowd-control plan, fire-safety approval, evacuation plan, accessibility assessment, or legal certification.

### Failure Handling
Validation issues remain visible. Invalid input must not be represented as a safe or capacity-compliant plan.

### Human Review
The event organizer and venue representative must review the plan and all safety arrangements before the event.

## Human Review and Safety
Always verify the legally approved capacity and venue instructions with responsible personnel. Confirm emergency exits, accessibility, staffing, crowd flow, and applicable local rules. Do not rely on this estimate alone for safety-critical decisions.

## Auditability
The calculation is reproducible from the supplied registration count, attendance rate, and capacity. Keep the original input and report so assumptions can be reviewed later.

## Global Limits
- The agent uses supplied assumptions and does not verify them externally.
- The attendance estimate is not guaranteed.
- Approved venue capacity must not be exceeded.
- The agent does not certify safety or legal compliance.
- Human review is required for every report.
