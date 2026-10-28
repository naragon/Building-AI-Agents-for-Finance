# Self-Consistency — Investment Recommendation Lab

An implementation of the **Self-Consistency** reasoning paradigm (Wang et al., 2022) applied to a finance task: producing an investment recommendation (`BUY` / `HOLD` / `SELL`) for a stock by sampling multiple independent chain-of-thought reasoning paths and selecting the plurality answer.

See `results-example.md` for a sample run.

## Requirements

- Python 3.12 (repository baseline)
- An Anthropic API key

## Setup

1. From the repository root, install the shared profile:

   ```powershell
   uv sync --locked --group chapter-6-anthropic
   .\.venv\Scripts\Activate.ps1
   cd "Chapter 6/chapter_6_lab_2_self-consistency"
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
