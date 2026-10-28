# Hands-on lab: Agentic RAG over financial documents with LlamaIndex

Companion code for the chapter **Building Agentic RAG Systems in Finance**.

## What it does

Builds, step by step, from a naive retrieve-then-generate pipeline to an agentic
RAG system that routes across heterogeneous financial documents, decomposes
comparative questions, and self-corrects by re-querying when the evidence is
insufficient. It then briefly adds reranking and answer evaluation.

The corpus (`data/`) is three small synthetic financial documents:

- `acme_10k_excerpt.md` — a 10-K annual-report excerpt
- `acme_earnings_call_q3.md` — a Q3 earnings-call transcript
- `firm_risk_policy.md` — an internal liquidity/risk policy

## Tech stack

- **LlamaIndex** for indexing, routing, decomposition, and the agent loop
- **Claude (`claude-sonnet-4-6`)** for generation/reasoning, via
  `llama-index-llms-anthropic`
- **OpenAI `text-embedding-3-small`** for the vector index

## Setup

Use Python 3.12 and uv >=0.13.1. Install from the **repository root**:

```bash
uv sync --locked --group chapter-10
source .venv/bin/activate
# Windows alternative: .\.venv\Scripts\Activate.ps1
cd "Chapter 10"
```

Run subsequent commands from this chapter folder using the activated root
environment. Dependencies and the single lockfile live at the repository root;
`requirements.txt` is a legacy reference. See the
[root setup guide](../README.md#package-management).

**3. Add your API keys**

```bash
cp .env.example .env        # Windows PowerShell: Copy-Item .env.example .env
```

Then edit `.env` and set **both** keys — the lab will not run without them:

```
ANTHROPIC_API_KEY=sk-ant-...   # Claude, for generation/reasoning
OPENAI_API_KEY=sk-...          # OpenAI, for embeddings
```

## Run

### Run the full pipeline
With the virtualenv activated and `.env` filled in, run the full pipeline:

```bash
python agentic_rag_lab.py
```

This runs steps 3→10 in sequence: naive RAG → router → sub-question decomposition →
self-correcting agent → hybrid search → reranking → hybrid + reranking (recall-then-
precision) → answer evaluation.

Each `step_*` function maps 1:1 to a numbered snippet in the chapter.

### Where the results go

Besides printing to the terminal, every step writes a markdown report to
`results/lab_runs/` — one file per step (e.g. `Step_4_router_query_engine.md`).
Each report records both the **retrieved context chunks** (which source document,
with its relevance score) and the **final answer**, so you can see *why* a step
answered the way it did, and how the patterns differ in what they retrieve.

A single shared question — *"Does Acme's Q3 quick ratio satisfy the firm's risk
policy?"* — is run through the retrieval-pattern steps (3–7 and the hybrid+rerank
step 9) and collected side by side in
`00_comparison_quick_ratio_policy.md`. That file is the quickest way to see the
progression: the naive baseline blends all sources, the router commits to one,
decomposition and the agent gather across sources, and hybrid search fuses recall.

### Run a single step

Each step can be run independently, straight from the terminal with `python -c`.
Steps **4, 5, 6, 8, and 10** operate on the shared per-document indices, so build
them first with `load_indices()` and pass the result in:

```bash
python -c "from agentic_rag_lab import load_indices, step_4_router; step_4_router(load_indices())"
python -c "from agentic_rag_lab import load_indices, step_5_subquestion; step_5_subquestion(load_indices())"
python -c "from agentic_rag_lab import load_indices, step_6_agent; step_6_agent(load_indices())"
python -c "from agentic_rag_lab import load_indices, step_8_rerank; step_8_rerank(load_indices())"
python -c "from agentic_rag_lab import load_indices, step_10_evaluate; step_10_evaluate(load_indices())"
```

Steps **3, 7, and 9** build their own index or retriever internally and take no
arguments:

```bash
python -c "from agentic_rag_lab import step_3_naive_rag; step_3_naive_rag()"
python -c "from agentic_rag_lab import step_7_hybrid; step_7_hybrid()"
python -c "from agentic_rag_lab import step_9_hybrid_rerank; step_9_hybrid_rerank()"
```

The same imports work from a notebook or REPL if you prefer to iterate interactively:

```python
from agentic_rag_lab import load_indices, step_4_router
indices = load_indices()
step_4_router(indices)
```

A single step run still writes its own report to `results/lab_runs/`, but the
side-by-side comparison file (`00_comparison_quick_ratio_policy.md`) is only
assembled at the end of a full pipeline run (`python agentic_rag_lab.py`), since it
aggregates the answers of steps 3–7 and 9 to the shared question.

The documents are intentionally small, so a full run is fast and cheap — but note that
**every step makes live, paid API calls** to Claude and OpenAI (it is not offline).
