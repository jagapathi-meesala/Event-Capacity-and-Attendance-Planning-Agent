from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
"agent.yaml","README.md","LICENSE","EXPLAINABILITY.md","core/__init__.py","core/engine.py","core/cli.py",
"tests/test_engine.py","tools/validate_event_plan.yaml","tools/estimate_attendance.yaml","tools/generate_capacity_report.yaml",
"skills/capacity-planning/SKILL.md","skills/attendance-forecasting/SKILL.md","skills/event-safety-review/SKILL.md",
"examples/event_plan.json","verification/readiness_audit.py"]
missing = [x for x in REQUIRED if not (ROOT/x).is_file()]
agent = (ROOT/"agent.yaml").read_text(encoding="utf-8")
match = re.search(r"^name:\s*([a-z][a-z0-9-]*)\s*$", agent, re.M)
explain = (ROOT/"EXPLAINABILITY.md").read_text(encoding="utf-8")
headings = ["## Purpose","## Inputs","## Decision","## Attendance Estimation","## Capacity Assessment",
"## Outputs and Evidence","## Tool: validate-event-plan","## Tool: estimate-attendance",
"## Tool: generate-capacity-report","## Human Review and Safety","## Auditability","## Global Limits"]
checks = {
"Required files": not missing,
"Agent name valid": bool(match) and match.group(1) == "event-capacity-attendance-planning-agent",
"Explainability sections": all(h in explain for h in headings)}
print(f"Required files: {len(REQUIRED)-len(missing)}/{len(REQUIRED)}")
for label, ok in checks.items(): print(f"{label}: {'PASS' if ok else 'FAIL'}")
if missing: print("Missing:", ", ".join(missing))
sys.exit(0 if all(checks.values()) else 1)
