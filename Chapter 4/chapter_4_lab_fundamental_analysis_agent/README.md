# Fundamental Analysis Agent — Lab

An AI-powered fundamental stock analysis pipeline built with the **OpenAI Agents SDK**.
Five specialist agents (financial data, valuation, news/sentiment, risk, report writer) collaborate under an Orchestrator to produce a professional investment brief for any publicly traded stock.

---

## What You'll Learn

- How to build a **multi-agent pipeline** with the OpenAI Agents SDK
- The **agents-as-tools** pattern (vs. handoffs) for keeping an Orchestrator in control
- How to run **parallel** vs **sequential** sub-agent phases
- How to wire pure Python functions as tools via `@function_tool`
- How to design agents whose outputs are structured enough to feed a synthesis step

---

## Architecture

```
OrchestratorAgent
  Phase 1 (parallel):   financial_data_analysis + news_and_sentiment_analysis + risk_assessment
  Phase 2 (after P1):   valuation_analysis        (needs financial context)
  Phase 3 (last):       write_investment_report   (synthesizes everything)
```

| Agent | Tools it owns |
|---|---|
| FinancialDataAgent | `get_income_statement`, `get_balance_sheet`, `get_cash_flow_statement`, `compute_key_ratios` |
| ValuationAgent | `run_dcf_model`, `get_peer_multiples` |
| NewsAndSentimentAgent | `search_recent_news`, `analyze_sentiment` |
| RiskAgent | `get_balance_sheet`, `compute_key_ratios`, `search_recent_news` |
| ReportWriterAgent | *(none — pure synthesis)* |

---

## Setup

### 1. Clone the repo and enter the folder

```bash
git clone <your-repo-url>
cd fundamental_analysis_agent
```

All commands from this point on assume your terminal is **inside the `fundamental_analysis_agent/` folder**.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
uv venv
.\.venv\Scripts\Activate.ps1
```
If activation is blocked by execution policy, run once:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**macOS / Linux:**
```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv sync --locked
```

### 4. Add your OpenAI API key

Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

Then edit `.env`:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Get a key at https://platform.openai.com/api-keys.

---

## Running the Lab

All commands below are run from **inside the `fundamental_analysis_agent/` folder**.

### Basic run

```bash
python main.py AAPL
```

### Useful flags

| Flag | What it does |
|---|---|
| `--watchlist TICKER ...` | Analyze multiple tickers sequentially (e.g. `--watchlist MSFT GOOGL`) |
| `--output FILE` | Save the final report to a text file |
| `--stream` | Stream the Orchestrator's tokens as they arrive |
| `--verbose` | Print each sub-agent's output to the terminal |
| `--trace` | Print raw tool-call sequence (great for verifying parallel execution) |
| `--log-dir DIR` | Save each sub-agent's output to its own `.txt` file inside `DIR` |
| `--working-memory [FILE]` | Mirror everything printed to the terminal into a file |

### Examples

**Basic — single ticker**
```bash
python main.py AAPL
```

**Watchlist — run several tickers sequentially**
```bash
python main.py AAPL --watchlist MSFT GOOGL NVDA
```

**Save the final report to a file**
```bash
python main.py AAPL --output report.txt
```

**Stream the Orchestrator's tokens as they arrive**
```bash
python main.py AAPL --stream
```

**Verbose — print every sub-agent's output to the terminal**
```bash
python main.py AAPL --verbose
```

**Trace — see the raw CALL/OUTPUT tool-call sequence (proves parallel execution)**
```bash
python main.py AAPL --trace
```

**Log every sub-agent's output to its own file**
```bash
python main.py AAPL --log-dir logs
```

**Working memory — mirror everything in the terminal to a file**
```bash
python main.py AAPL --working-memory                  # default: working_memory.txt
python main.py AAPL --working-memory run1.txt         # custom filename
```

**Combine flags — verbose + trace + per-agent log files**
```bash
python main.py AAPL --verbose --trace --log-dir logs
```

**Full workflow — watchlist, streamed, with logs and a saved final report**
```bash
python main.py AAPL --watchlist MSFT GOOGL NVDA \
    --stream --verbose --log-dir logs --output report.txt
```

**Show the help message**
```bash
python main.py --help
```

When you use `--log-dir DIR`, the following files are written:

```
DIR/<TICKER>_financial_data_analysis.txt
DIR/<TICKER>_news_and_sentiment_analysis.txt
DIR/<TICKER>_risk_assessment.txt
DIR/<TICKER>_valuation_analysis.txt
DIR/<TICKER>_write_investment_report.txt
DIR/<TICKER>_final_report.txt
```

---

## Project Layout

```
fundamental_analysis_agent/        ← repo root (you run commands from here)
├── README.md                      ← you are here
├── requirements.txt
├── .env.example                   ← template — copy to .env and fill in your key
├── .gitignore
├── __init__.py
├── main.py                        ← CLI entry point + analyze_ticker / analyze_watchlist
├── specialist_agents/             ← Agent definitions (instructions + tool wiring)
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── financial_data_agent.py
│   ├── valuation_agent.py
│   ├── news_sentiment_agent.py
│   ├── risk_agent.py
│   └── report_writer_agent.py
└── tools/                         ← Pure Python @function_tool wrappers around yfinance
    ├── __init__.py
    ├── cache.py
    ├── financial_tools.py
    ├── valuation_tools.py
    └── news_tools.py
```

Note: the package folder is called `specialist_agents/` (not just `agents/`) on purpose — the OpenAI Agents SDK exposes a top-level `agents` package, and we don't want our local folder to shadow it.

---

## Lab Exercises (Suggested)

1. **Trace parallelism.** Run with `--trace` and check that the three Phase 1 agents are all `CALL`ed before any `OUTPUT` appears.
2. **Add a new sector.** Pick a ticker whose sector is missing from `SECTOR_PEERS` in `tools/valuation_tools.py` — add the peer list and re-run.
3. **Tune the DCF.** Modify the baselines (growth=8%, discount=9%, terminal=3%) in `specialist_agents/valuation_agent.py` and observe how the intrinsic value changes.
4. **Add a sixth agent.** For example, a `MacroAgent` that pulls Fed rate and inflation context. Wire it into the Orchestrator's Phase 1.
5. **Swap the model.** Try `gpt-4o-mini` for one of the specialist agents (not the Orchestrator or ReportWriter) and compare quality.

---

## Troubleshooting

- **`OPENAI_API_KEY is not set`** — confirm `.env` exists in this folder (the same folder as `main.py`) and contains a real key.
- **`ModuleNotFoundError: specialist_agents`** or **`ModuleNotFoundError: tools`** — you're running from the wrong folder. `cd` into the `fundamental_analysis_agent/` folder first.
- **`Activate.ps1 cannot be loaded`** — set PowerShell execution policy: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
- **yfinance returns no data** — Yahoo occasionally throttles or temporarily returns empty data; retry after a minute.
- **Empty news results** — Yahoo's news feed can be sparse for less-followed tickers; this is expected.

---

## Disclaimer

This project is for **educational purposes only**. Reports generated by this agent are not investment advice. Always do your own research before making any financial decisions.
