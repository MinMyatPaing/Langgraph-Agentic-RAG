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

## Contributing

- Follow the current code conventions in the repo.
- Prefer small, focused PRs: tests, type hints, one functional change per PR.
