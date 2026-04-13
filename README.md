# AIAutomationDev

> An AI-native open-source repository for building and maintaining software projects with an AI developer in the loop.

## AI Disclosure

This repository is **primarily initiated and maintained by an AI developer** operating under human ownership and oversight.

That is not a metaphor:
- the project direction may be proposed by an AI,
- code, docs, and maintenance chores may be produced by an AI,
- and the repository exists in part to explore what **long-term AI open-source maintenance** actually looks like in practice.

## Purpose

AIAutomationDev aims to become a practical toolkit for **AI-first repository maintenance**:
- turning vague project intent into a concrete roadmap,
- generating lightweight maintenance reports,
- helping AI agents keep a repo healthy over time,
- and documenting transparent AI contribution workflows.

The first milestone is intentionally small: a local CLI that can inspect a repository and generate a structured maintenance report.

## Why this project

Most AI coding demos stop at “generate code once”. Real open source work is different:
- projects need repeated maintenance,
- context has to survive over time,
- documentation matters,
- and transparency about AI authorship matters.

This repo is meant to be a living experiment in that direction.

## Current scope (MVP)

The MVP provides a Python CLI that can:
- scan a local repository,
- summarize basic repository signals,
- and emit a Markdown maintenance report.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
aad weekly-report --repo . --format markdown
```

## Example output

```bash
aad weekly-report --repo . --format markdown --output WEEKLY_REPORT.md
```

The `--output` flag lets you save the generated report directly from the CLI, which is handy for scheduled maintenance jobs and automation scripts.

## Roadmap

### v0.1
- [x] Bootstrap repository
- [x] Add transparent AI-maintainer README
- [x] Implement local repository maintenance report CLI
- [ ] Add richer git history summarization
- [ ] Add configurable ignore patterns

### v0.2
- [ ] Add issue/PR ingestion via GitHub API or `gh`
- [ ] Add repository health scoring
- [ ] Add machine-readable JSON report schema

### v0.3
- [ ] Add agent workflow templates for recurring maintenance
- [ ] Add changelog draft generation
- [ ] Add task suggestion engine

## Project principles

1. **AI authorship should be explicit.**
2. **Human oversight should remain possible.**
3. **Maintenance is a first-class feature.**
4. **Useful before impressive.**

## License

MIT
