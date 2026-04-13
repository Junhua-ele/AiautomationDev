from pathlib import Path
import tempfile
import subprocess

from aiautomationdev.cli import main
from aiautomationdev.report import build_report, _extract_changed_files


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


def test_weekly_report_can_write_output_file(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)

    output_path = tmp_path / "reports" / "weekly.md"
    exit_code = main([
        "weekly-report",
        "--repo",
        str(repo),
        "--output",
        str(output_path),
    ])

    assert exit_code == 0
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "# Weekly Maintenance Report" in content
    assert f"- Path: `{repo.resolve()}`" in content


def test_extract_changed_files_preserves_full_paths():
    changed = _extract_changed_files([
        "M README.md",
        "?? src/aiautomationdev/cli.py",
        "A  tests/test_report.py",
    ])

    assert changed == [
        "README.md",
        "src/aiautomationdev/cli.py",
        "tests/test_report.py",
    ]
