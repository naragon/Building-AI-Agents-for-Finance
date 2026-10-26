# Self-Refine — Investment Thesis Lab

An implementation of the **Self-Refine** reasoning paradigm (Madaan et al., 2023) applied to a finance task: drafting an equity investment thesis from a small block of financial metrics, then iteratively critiquing and refining it using a single LLM as generator, feedback provider, and refiner.

See `results-example.md` for a sample run.

## Requirements

- Python 3.9+
- An Anthropic API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   uv venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   uv sync --locked
   ```

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
