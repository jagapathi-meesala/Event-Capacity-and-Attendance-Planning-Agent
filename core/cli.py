import argparse
import json
from pathlib import Path
from .engine import generate_report

def main():
    parser = argparse.ArgumentParser(description="Estimate event attendance against stated venue capacity.")
    parser.add_argument("input", help="Path to event plan JSON")
    parser.add_argument("--output", default="-", help="Report output path or '-' for stdout")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = generate_report(payload)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output == "-":
        print(rendered)
    else:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    if report.get("status") == "needs_input_correction":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
