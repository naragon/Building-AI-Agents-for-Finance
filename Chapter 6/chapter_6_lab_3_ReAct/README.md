# ReAct Lab

A ReAct agent that analyzes whether a stock is overvalued vs. its sector, built on the **Claude Agent SDK** with live financial data from `yfinance`.

The agent alternates **Thought → Action → Observation** steps, printed to the console, and produces a final recommendation.

## Prerequisites

- Python 3.10+
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

### 1. Create a virtual environment

```powershell
# Windows (PowerShell)
uv venv
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
uv venv
source .venv/bin/activate
```

If PowerShell blocks the activation script, allow it for the current user once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install dependencies

```powershell
uv sync --locked
```

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
