# Tree of Thoughts — Hedge Selection Lab

A minimal implementation of the **Tree of Thoughts (ToT)** reasoning paradigm (Yao et al., 2023) applied to a finance task: choosing how to hedge a concentrated single-name equity position into a binary catalyst (earnings).

The script explores hedge candidates as a tree, scores each branch with the LLM acting as evaluator, and uses **beam search** to retain the top branches at each level:

- **Level 1** — propose distinct hedge instruments (e.g., puts, put spreads, sector hedges, covered calls), score each on protection / cost / basis risk, keep the top `beam_width`.
- **Level 2** — for each retained hedge, propose distinct sizings/structures (strike, notional, expiry, spread width), score each, keep the best.

See `tot-example.md` for a sample run.

## Requirements

- Python 3.12 (repository baseline)
- An Anthropic API key

## Setup

1. From the repository root, install the shared profile:

   ```powershell
   uv sync --locked --group chapter-6-anthropic
   .\.venv\Scripts\Activate.ps1
   cd "Chapter 6/chapter_6_lab_4_ToT"
   ```

2. On macOS/Linux use `source .venv/bin/activate` at the root instead.
   Dependencies and `uv.lock` live at the repository root; `requirements.txt`
   is a legacy reference. See the [root setup guide](../../README.md#package-management).

3. Copy `.env.example` to `.env` and fill in your API key:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   The `.env` file is gitignored.

## Run

```powershell
python tot.py
```

The script prints, at each level, the candidates generated, the per-candidate scores, the retained beam, and finally a one-line summary of each retained hedge with its best sizing.

## Configuration

Edit the constants near the top of `tot.py`:

- `MODEL` — Anthropic model id (default: `claude-sonnet-4-6`).

The `beam_width` (level-1 beam) and the `n` arguments to `generate_hedges` / `generate_sizings` (branching factor) are passed as function arguments inside `best_hedges`.

## Files

- `tot.py` — the lab script.
- `tot-example.md` — sample output from a previous run.
- `requirements.txt` — Python dependencies.
- `.env.example` — template for the API key.
