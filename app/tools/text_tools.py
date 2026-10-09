from langchain_core.tools import tool


@tool
def normalize_learning_topic(topic: str) -> str:
    """Normalize a single learning topic for consistent catalog searches.

    Trims surrounding whitespace and collapses repeated internal whitespace.
    It does not infer synonyms, translate terms, or search the resource catalog.
    """
    normalized = " ".join(topic.split())
    if not normalized:
        raise ValueError("topic cannot be empty or whitespace-only")
    return normalized
