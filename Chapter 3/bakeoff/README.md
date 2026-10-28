# Chapter 3 — framework bake-off

The same finance "Hello World" task — fetch AAPL and JPM price/EPS,
compute P/E ratios, write a comparison memo — implemented in eight
frameworks. All implementations share `common.py` (mock data, prompts,
tools, output capture), so differences in the outputs reflect the
frameworks, not the inputs.

| File | Framework | Needs |
|---|---|---|
| `openai_agents_sdk_agent.py` | OpenAI Agents SDK | `OPENAI_API_KEY` |
| `langchain_agent.py` | LangChain 1.0 `create_agent` | `OPENAI_API_KEY` |
| `autogen_agent.py` | AutoGen (AgentChat) | `OPENAI_API_KEY` |
| `pydantic_ai_agent.py` | PydanticAI | `OPENAI_API_KEY` |
| `llamaindex_agent.py` | LlamaIndex `FunctionAgent` | `OPENAI_API_KEY` |
| `crewai_agent.py` | CrewAI | `OPENAI_API_KEY` |
| `google_adk_agent.py` | Google ADK | `GOOGLE_API_KEY` |
| `mistral_agent.py` | Mistral (function calling) | `MISTRAL_API_KEY` |
| `claude_agent_sdk_agent.py` | Claude Agent SDK | `ANTHROPIC_API_KEY` |

(LangChain and LlamaIndex share one slot in the chapter's count of
eight; both files are provided.)

## Run

Framework profiles and the single lockfile now live at the repository root
(Python 3.12, uv >=0.13.1). From the **repository root**:

```bash
uv sync --locked --group chapter-3-openai-agents
export OPENAI_API_KEY=...         # plus provider keys as needed
cd "Chapter 3/bakeoff"
uv run --project ../.. --locked --group chapter-3-openai-agents python openai_agents_sdk_agent.py
```

Choose the matching root group: `chapter-3-openai-agents`, `chapter-3-langchain`,
`chapter-3-autogen`, `chapter-3-pydantic-ai`, `chapter-3-llamaindex`,
`chapter-3-bakeoff-mistral`, `chapter-3-crewai`, `chapter-3-google-adk`, or
`chapter-3-claude-agent-sdk`. The separate Mistral bake-off group preserves its
original pin; `chapter-3-mistral` is for the notebook. Only one profile may be
selected at a time. `requirements.txt` is a historical combined package list,
not an installation target. See the [root setup guide](../../README.md#package-management).

Each run prints the memo plus measured token usage and writes both to
`outputs/<framework>.txt`. The captured outputs in `outputs/` are from
real runs (gpt-5-mini for the OpenAI-backed frameworks,
gemini-2.5-flash for ADK). Data is mocked in `common.py` for
deterministic, key-free reproduction — swapping in yfinance or a vendor
feed is a one-line change there.
