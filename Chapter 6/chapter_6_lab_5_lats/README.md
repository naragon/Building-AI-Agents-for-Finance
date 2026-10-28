# LATS: Language Agent Tree Search

A minimal reference implementation of **Language Agent Tree Search** ([Zhou et al., 2023](https://arxiv.org/abs/2310.04406)) built on the [Claude Agent SDK](https://docs.anthropic.com/en/docs/claude-agent-sdk). LATS unifies reasoning, acting, and planning by combining LLM-driven agents with Monte Carlo Tree Search.

The task is intentionally toy — trimming a simulated tech-sector portfolio from 40% exposure down to a 30% target — so the focus stays on the search algorithm, not the domain.

## How it works

```
            root (40.0%)
           /            \
      c1 (33.6%)     c2 (36.0%)        ← Iteration 1: expand root
      /       \       /       \
  c1/c1    c1/c2  c2/c1    c2/c2       ← Iterations 2-3: UCT-guided descent
 (32.2%)  (32.2%) (33.6%) (33.6%)
```

Each iteration runs four steps:

1. **Selection** — descend from root via UCT (Upper Confidence Bound for Trees), balancing exploitation of high-scoring branches against exploration of less-visited ones.
2. **Expansion** — the LM proposes *k* distinct candidate actions in a single call (one-shot k-expand). Each is applied to a copy of the parent state via a pure environment function.
3. **Evaluation** — the LM scores each new child state on a 1-10 rubric (normalized to [0, 1] for UCT compatibility).
4. **Backpropagation** — scores propagate from new leaves back to the root, updating running-average values at every ancestor.

On failure, a **Backpropagation** and **reflection** steps are performed. The latest one generates a `When <situation>, do <action>` lesson that is prepended to the next iteration's prompt as long-term memory.

## Project structure

```
lats/
├── lats_search.py          # LATS algorithm: Node, UCT, select, expand, backprop, driver
├── lats_helpers.py          # Environment, LM-call wrappers, parsers, output utilities
├── requirements.txt         # claude-agent-sdk, anyio, python-dotenv
├── .claude/
│   └── skills/
│       ├── trade-evaluator/ # Scoring rubric for the evaluation step
│       └── trade-reflector/ # Reflection template for the failure path
└── .env                     # ANTHROPIC_API_KEY (not committed)
```

## Setup

### Prerequisites

- Python 3.12 (repository baseline)
- Node.js (the Claude Agent SDK spawns the Node-based `claude` CLI under the hood)
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
# From the repository root:
uv sync --locked --group chapter-6-claude-agent-sdk
# Linux/macOS
source .venv/bin/activate
# Windows alternative: .\.venv\Scripts\Activate.ps1
cd "Chapter 6/chapter_6_lab_5_lats"

# Install the Claude CLI globally
npm install -g @anthropic-ai/claude-code
```

Dependencies and the lockfile are managed at the root; `requirements.txt` is
a legacy reference. See the [root setup guide](../../README.md#package-management).

### Configure

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### Run

```bash
python lats_search.py
```

Tune the search parameters at the bottom of `lats_search.py`:

```python
anyio.run(lats_search, 3, 2, 3)
#                      │  │  └── max_depth
#                      │  └───── k_expand (candidates per expansion)
#                      └──────── n_iterations
```

## Running in Google Colab

The Claude Agent SDK requires Node.js in addition to the Python package:

```python
!apt-get -qq install -y nodejs npm #Could be already available in Google colab, go to N°3
!npm install -g @anthropic-ai/claude-code #Could be already available in Google colab, go to N°3
!uv pip install --system -q claude-agent-sdk anyio python-dotenv
```

Stage all files (including `.claude/skills/`) under one working directory and set the API key:

```python
import os
from google.colab import userdata
os.environ["ANTHROPIC_API_KEY"] = userdata.get("ANTHROPIC_API_KEY")
```

Run with `await` (Colab is already inside an event loop):

```python
await lats_search(3, 2, 3)
```

## Example output

```
=== Iteration 1 ===
Selected: root (depth=0, N=0, V=0.00)
  [add ] root/c1: positions=['NVDA', 'MSFT'] pct=8.0  score=4.0/10  V=0.40  exposure=33.6%
  [add ] root/c2: positions=['AAPL', 'GOOGL', 'META', 'AMD'] pct=2.5  score=5.0/10  V=0.50  exposure=36.0%
  [lesson] When starting exposure exceeds the target by more than the sum of planned
           per-name trims, do increase individual slice sizes so the aggregate trim
           equals or exceeds the full required reduction.

=== Iteration 2 ===
Selected: root/c2 (depth=1, N=1, V=0.50)
  [add ] root/c2/c1: positions=['NVDA', 'MSFT'] pct=3.0  score=4.0/10  V=0.40  exposure=33.6%
  [add ] root/c2/c2: positions=['AAPL', 'GOOGL', 'META', 'AMZN'] pct=1.5  score=2.0/10  V=0.20  exposure=33.6%

=== Iteration 3 ===
Selected: root/c1 (depth=1, N=1, V=0.40)
  [add ] root/c1/c1: positions=['NVDA', 'MSFT', 'AAPL'] pct=1.2  score=5.0/10  V=0.50  exposure=32.2%
  [add ] root/c1/c2: positions=['NVDA', 'META'] pct=1.8  score=4.0/10  V=0.40  exposure=32.2%

=== Final tree ===
root: N=6 V=0.40 exposure=40.0%
  root/c1: N=3 V=0.43 exposure=33.6%
    root/c1/c1: N=1 V=0.50 exposure=32.2%
    root/c1/c2: N=1 V=0.40 exposure=32.2%
  root/c2: N=3 V=0.37 exposure=36.0%
    root/c2/c1: N=1 V=0.40 exposure=33.6%
    root/c2/c2: N=1 V=0.20 exposure=33.6%

Best leaf: root/c1/c1  V=0.50  exposure=32.2%
```

Notice how iteration 3 pivots back to `root/c1` instead of drilling deeper into `root/c2`. After iteration 2, backpropagation lowered `c2`'s value from 0.50 to 0.37 (its children underperformed), while `c1` remained at 0.40 with only one visit. UCT's exploration term compounds this: `c1` wins on both exploitation *and* exploration. This is the MCTS feedback loop in action — deep exploration corrects early overestimates.

## Deviations from the paper

Two intentional simplifications:

1. **No rollout-to-terminal within a single iteration.** The paper prescribes that simulation continues expand-evaluate-select all the way to a terminal state within one iteration. This implementation expands by one depth per iteration (the "value-network" approach used by AlphaGo, Leela, and MuZero), trusting the leaf evaluator's score in lieu of a full rollout. Per-iteration LM cost stays at `1 + k` instead of growing with depth.

2. **No self-consistency scoring.** The paper combines a self-generated score with a self-consistency score (rewarding actions that are proposed repeatedly under sampling). This implementation uses the single evaluator score only.

## Key formulas

**UCT** (selection):

```
UCT(s) = V(s) + w * sqrt(ln(N(parent)) / N(s))
```

**Value update** (backpropagation):

```
V_new(s) = (V_old(s) * (N(s) - 1) + r) / N(s)
```

Where `V(s)` is the running-average value in [0, 1], `N(s)` is the visit count, `w = 1.41` is the exploration weight, and `r` is the normalized reward from the evaluator.

## License

MIT
