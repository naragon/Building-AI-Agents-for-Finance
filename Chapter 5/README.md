# Chapter 5 — Deep search: analyst-grade research with AI agents

Two ways to work through this chapter's code:

- **Lab notebooks** (start here):
  - `chapter_5_lab_1_deep_search_planner.ipynb` — the planner in isolation:
    decompose a research question into typed, dependency-ordered sub-tasks.
  - `chapter_5_lab_2_deep_search_full_pipeline.ipynb` — the full pipeline:
    planner, researcher, validator, and synthesizer working end to end.
- **`src/`** — the complete project the chapter walks through
  (`planner.py`, `researcher.py`, `validator.py`, `synthesizer.py`,
  `tools/`, shared `common.py`), plus the figure sources under
  `src/diagrams/`. From the repository root, install with
  `uv sync --locked --group chapter-5`, then run with
  `uv run --locked --group chapter-5 python "Chapter 5/src/deep_search_agent.py"`.
  Set the API keys named in the chapter's Technical requirements.

For local notebooks, add `--group notebooks` and launch Jupyter with the same
root profile. Skip notebook package-installation cells locally; they are for
Colab and bypass the lockfile. See the [root setup guide](../README.md#package-management).
