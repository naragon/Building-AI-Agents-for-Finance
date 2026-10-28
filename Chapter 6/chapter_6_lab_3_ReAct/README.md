# ReAct Lab

A ReAct agent that analyzes whether a stock is overvalued vs. its sector, built on the **Claude Agent SDK** with live financial data from `yfinance`.

The agent alternates **Thought → Action → Observation** steps, printed to the console, and produces a final recommendation.

## Prerequisites

- Python 3.12 (repository baseline)
- Node.js 18+ (the Claude Agent SDK launches the Claude Code CLI under the hood)
- An Anthropic API key

Install the Claude Code CLI once globally:

```powershell
npm install -g @anthropic-ai/claude-code
```

Set your API key:

```powershell
# PowerShell (current session)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# PowerShell (persist for the user)
setx ANTHROPIC_API_KEY "sk-ant-..."
```

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Setup

From the repository root:

```powershell
uv sync --locked --group chapter-6-claude-agent-sdk
.\.venv\Scripts\Activate.ps1
cd "Chapter 6/chapter_6_lab_3_ReAct"
```

On macOS/Linux use `source .venv/bin/activate` at the root instead.
The root profile and lockfile replace per-lab environments; see the
[root setup guide](../../README.md#package-management).

## Run

```powershell
python react.py
```

You should see a trace like:

```
[THOUGHT] Thought: I need AAPL's valuation multiples first...
[ACTION] get_valuation_ratios({'ticker': 'AAPL'})
[OBSERVATION] {"PE": 32.1, "EV_EBITDA": 24.5, ...}
[THOUGHT] Now I need the sector median to benchmark...
[ACTION] get_sector_median_pe({'sector': 'Technology'})
...
============================================================
FINAL ANSWER
============================================================
...
```

## How it works

- `react.py` defines three MCP tools via `@tool`: `get_valuation_ratios`, `get_sector_median_pe`, `get_balance_sheet`.
- All three tools query Yahoo Finance live through `yfinance`.
- Sector medians are computed on the fly across a curated list of large-cap tickers per GICS sector.
- `ClaudeSDKClient` streams the assistant's response; the script prints each text block as `[THOUGHT]`, each tool call as `[ACTION]`, and each tool result as `[OBSERVATION]`.

## Customize

- Change the question at the bottom of `react.py`.
- Add or swap tickers in `SECTOR_TICKERS` to widen sector coverage.
- Swap the model via the `model=` argument in `ClaudeAgentOptions` (e.g., `claude-opus-4-7`).
