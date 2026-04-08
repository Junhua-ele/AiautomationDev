from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import subprocess
from typing import Iterable


@dataclass
class RepoReport:
    repo_path: str
    branch: str
    tracked_files: int
    recent_commits: list[str]
    changed_files: list[str]
    top_level_entries: list[str]

    def as_dict(self) -> dict:
        return {
            "repo_path": self.repo_path,
            "branch": self.branch,
            "tracked_files": self.tracked_files,
            "recent_commits": self.recent_commits,
            "changed_files": self.changed_files,
            "top_level_entries": self.top_level_entries,
        }


def _run_git(repo: Path, *args: str) -> str:
    cmd = ["git", "-C", str(repo), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _safe_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def build_report(repo: str | Path) -> RepoReport:
    repo = Path(repo).resolve()
    branch = _run_git(repo, "branch", "--show-current") or "unknown"

    tracked_output = _run_git(repo, "ls-files")
    tracked_files = len(_safe_lines(tracked_output))

    recent_output = _run_git(repo, "log", "--oneline", "-n", "5")
    recent_commits = _safe_lines(recent_output)

    changed_output = _run_git(repo, "status", "--short")
    changed_files = _extract_changed_files(_safe_lines(changed_output))

    top_level_entries = sorted(path.name for path in repo.iterdir() if path.name != ".git")

    return RepoReport(
        repo_path=str(repo),
        branch=branch,
        tracked_files=tracked_files,
        recent_commits=recent_commits,
        changed_files=changed_files,
        top_level_entries=top_level_entries,
    )


def _extract_changed_files(lines: Iterable[str]) -> list[str]:
    changed = []
    for line in lines:
        if len(line) <= 3:
            continue
        changed.append(line[3:].strip())
    return changed


def render_markdown(report: RepoReport) -> str:
    recent = "\n".join(f"- {item}" for item in report.recent_commits) or "- No commits yet"
    changed = "\n".join(f"- {item}" for item in report.changed_files) or "- No working tree changes"
    entries = "\n".join(f"- {item}" for item in report.top_level_entries) or "- Empty repository"

    return f"""# Weekly Maintenance Report

## Repository
- Path: `{report.repo_path}`
- Branch: `{report.branch}`
- Tracked files: `{report.tracked_files}`

## Recent commits
{recent}

## Working tree changes
{changed}

## Top-level entries
{entries}
"""


def render_json(report: RepoReport) -> str:
    return json.dumps(report.as_dict(), indent=2, ensure_ascii=False)
