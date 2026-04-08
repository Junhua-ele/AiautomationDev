from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .report import build_report, render_json, render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aad", description="AI Automation Dev CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    weekly = subparsers.add_parser("weekly-report", help="Generate a repository maintenance report")
    weekly.add_argument("--repo", default=".", help="Repository path")
    weekly.add_argument("--format", choices=["markdown", "json"], default="markdown")

    args = parser.parse_args(argv)

    if args.command == "weekly-report":
        repo_path = Path(args.repo).resolve()
        if not repo_path.exists():
            parser.error(f"Repository path does not exist: {repo_path}")
        report = build_report(repo_path)
        if args.format == "json":
            print(render_json(report))
        else:
            print(render_markdown(report))
        return 0

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    sys.exit(main())
