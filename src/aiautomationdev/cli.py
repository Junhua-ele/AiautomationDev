from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .report import build_report, render_json, render_markdown


def _render_report(repo_path: Path, output_format: str) -> str:
    report = build_report(repo_path)
    if output_format == "json":
        return render_json(report)
    return render_markdown(report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aad", description="AI Automation Dev CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    weekly = subparsers.add_parser("weekly-report", help="Generate a repository maintenance report")
    weekly.add_argument("--repo", default=".", help="Repository path")
    weekly.add_argument("--format", choices=["markdown", "json"], default="markdown")
    weekly.add_argument("--output", help="Write the rendered report to a file instead of stdout")

    args = parser.parse_args(argv)

    if args.command == "weekly-report":
        repo_path = Path(args.repo).resolve()
        if not repo_path.exists():
            parser.error(f"Repository path does not exist: {repo_path}")

        rendered = _render_report(repo_path, args.format)

        if args.output:
            output_path = Path(args.output).expanduser()
            if not output_path.is_absolute():
                output_path = Path.cwd() / output_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(f"{rendered}\n", encoding="utf-8")
        else:
            print(rendered)
        return 0

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    sys.exit(main())
