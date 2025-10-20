from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of the graph

    Attributes:
        question: question prompt
        generation: LLM generation
        web_search: whether to add search or not
        documents: list of docs
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]
