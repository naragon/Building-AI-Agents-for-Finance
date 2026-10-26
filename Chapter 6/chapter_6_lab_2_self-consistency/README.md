# Self-Consistency — Investment Recommendation Lab

An implementation of the **Self-Consistency** reasoning paradigm (Wang et al., 2022) applied to a finance task: producing an investment recommendation (`BUY` / `HOLD` / `SELL`) for a stock by sampling multiple independent chain-of-thought reasoning paths and selecting the plurality answer.

See `results-example.md` for a sample run.

## Requirements

- Python 3.10+ (the script uses `str | None` typing syntax)
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
python self-consistency.py
```

The script prints each sampled reasoning path with its parsed recommendation, then the final vote breakdown and the majority recommendation.

## Configuration

Edit the constants near the top of `self-consistency.py`:

- `MODEL` — Anthropic model id (default: `claude-sonnet-4-6`).
- `N_PATHS` — number of independent reasoning paths to sample (default: `5`).
- `TEMPERATURE` — sampling temperature; controls path diversity (default: `0.8`).
In later Claude versions after Claude Sonnet 4.6, temperature can no longer be configured. Self-consistency is still applied with the default temperature.

A higher temperature produces more diverse reasoning chains; a lower one makes the paths converge and reduces the value of the majority vote. The Wang et al. (2022) paper reports the pattern is robust across reasonable temperature settings — the default of `0.8` is a sensible starting point for financial reasoning.

## Files

- `self-consistency.py` — the lab script.
- `results-example.md` — sample output from a previous run.
- `requirements.txt` — Python dependencies.
