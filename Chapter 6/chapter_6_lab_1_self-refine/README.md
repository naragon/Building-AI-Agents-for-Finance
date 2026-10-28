# Self-Refine — Investment Thesis Lab

An implementation of the **Self-Refine** reasoning paradigm (Madaan et al., 2023) applied to a finance task: drafting an equity investment thesis from a small block of financial metrics, then iteratively critiquing and refining it using a single LLM as generator, feedback provider, and refiner.

See `results-example.md` for a sample run.

## Requirements

- Python 3.12 (repository baseline)
- An Anthropic API key

## Setup

1. From the repository root, install the shared profile:

   ```powershell
   uv sync --locked --group chapter-6-anthropic
   .\.venv\Scripts\Activate.ps1
   cd "Chapter 6/chapter_6_lab_1_self-refine"
   ```

2. On macOS/Linux use `source .venv/bin/activate` at the root instead.
   Dependencies and `uv.lock` live at the repository root; `requirements.txt`
   is a legacy reference. See the [root setup guide](../../README.md#package-management).

3. Create a `.env` file in this folder with your API key:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   The `.env` file is gitignored.

## Run

```powershell
python self-refine.py
```

The script prints the initial thesis, then for each iteration the feedback and the refined thesis, and finally the converged thesis.

## Configuration

Edit the constants near the top of `self-refine.py`:

- `MODEL` — Anthropic model id (default: `claude-sonnet-4-6`).
- `MAX_ITERATIONS` — maximum number of feedback/refine rounds (default: `3`).

The loop also stops early if the feedback step returns a line beginning with `NO_FURTHER_FEEDBACK`.

## Files

- `self-refine.py` — the lab script.
- `results-example.md` — sample output from a previous run.
- `requirements.txt` — Python dependencies.
