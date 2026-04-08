from pathlib import Path
import tempfile
import subprocess

from aiautomationdev.report import build_report


def test_build_report_on_git_repo():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
        (repo / "README.md").write_text("hello\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        report = build_report(repo)
        assert report.repo_path == str(repo.resolve())
        assert report.tracked_files == 1
        assert "README.md" in report.top_level_entries
