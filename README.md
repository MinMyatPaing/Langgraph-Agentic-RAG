# Langgraph-Agentic-RAG

A small experimental repository that wires together a tiny graph of nodes for Retrieval-Augmented Generation (RAG). The project demonstrates:

- basic node implementations (retrieve, web_search, generate, etc.)
- a simple GraphState TypedDict to track question/generation/documents
- how nodes produce partial state updates which callers should merge into the running state

This README explains how to set up and run the project locally and documents the node contract and common troubleshooting steps.

## Quick facts

- Language: Python 3.10+ (use the project's virtualenv)
- Entrypoint: `main.py`
- Graph nodes live in `graph/nodes/` and return a `dict` with the keys they produce or modify.

## Project layout (important files)

- `main.py` — example entrypoint that invokes the graph
- `ingestion.py` — builds a Chroma vectorstore and retriever
- `graph/state.py` — `GraphState` TypedDict describing expected keys
- `graph/nodes/` — node functions (each returns a partial state dict)
- `graph/chains/` — LLM prompt/chain wiring

## Node return contract

Nodes should return a mapping (dict) containing only the keys they produce or update. Example:

- `web_search(state)` may return `{"documents": documents, "question": question}`
- `retrieve(state)` may return `{"documents": documents, "question": question}`
- `generate(state)` may return `{"generation": text, "question": question}`

The caller/executor is expected to merge node results into the running state, e.g. `state.update(node_result)`.

Notes about mutability: if a node modifies a mutable value (like appending to a documents list) be explicit about whether you intend to mutate in-place or return a new value. To keep semantics clear, prefer returning a new list (e.g., `new_docs = state.get("documents", []) + [new_doc]`) and returning `{"documents": new_docs}`.

## Prerequisites

- Python 3.10+
- A virtual environment (recommended)
- Project dependencies are declared in `pyproject.toml`.

## Recommended local setup (Windows, using bash)

From the project root:

```bash
# create and activate venv (if you haven't already)
python -m venv .venv
source .venv/Scripts/activate

# Install dependencies (editable install uses pyproject.toml)
pip install -e .
```

If you prefer to install exact packages listed elsewhere, use the relevant method you normally use (pip, poetry, etc.).

## Run the example

You can run the `main.py` entrypoint with the project's venv Python. Example (from repo root):

```bash
"C:/Users/minmy/Desktop/Code/LLM and Rag/langgraph-agentic-rag/.venv/Scripts/python.exe" "c:/Users/minmy/Desktop/Code/LLM and Rag/langgraph-agentic-rag/main.py"
```

Expected behavior:

- The script prints a short greeting and (if the chains and tools are configured) will invoke the graph app to produce a generation.

Potential runtime errors to watch for

- ImportError from `langchainhub`: some versions of `langchainhub` no longer expose the same `hub` API. If running `main.py` raises an ImportError from `graph/chains/generation.py`, either:

  - Install a compatible `langchainhub` version (see `pyproject.toml`), or
  - Replace/patch the generation chain to use a local prompt template or the new LangSmith APIs.

- Chroma/retriever duplication: if you see code that creates multiple Chroma instances pointing at the same `persist_directory`, prefer reusing the `Chroma` instance and calling `.as_retriever()` on it to avoid duplicate clients and repeated embedding initialization.

## Suggested improvements (low risk)

- Implement a small graph executor in `graph/graph.py` that accepts an initial state and a list of node functions and merges results automatically. That will make the contract explicit and reduce accidental state replacement.
- Add unit tests asserting executor merge behavior (happy path + mutation vs. immutability for `documents`).
- Add a small local prompt fallback in `graph/chains/generation.py` so `main.py` can run without network access or a specific hub client.

## Troubleshooting

- If you hit credential or API errors (OpenAI, LangChainHub, etc.), set the expected environment variables in a `.env` file or in your shell:

```bash
# examples (set the correct values for your setup)
export OPENAI_API_KEY="sk-..."
export LANGCHAIN_HUB_API_KEY="..."
```

- If `main.py` fails complaining about `hub.pull` or similar, check `graph/chains/generation.py` and consider adding a fallback prompt or stubbing the chain for local testing.

## Contributing

- Follow the current code conventions in the repo.
- Prefer small, focused PRs: tests, type hints, one functional change per PR.

## Contact / Next steps

If you want, I can:

- Add a minimal graph executor that merges node outputs into `state` and a unit test for it.
- Add a local fallback prompt for generation so `main.py` runs reliably without a specific `langchainhub` version.

Pick one and I'll implement it.
