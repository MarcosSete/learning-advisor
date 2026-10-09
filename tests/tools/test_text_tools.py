import pytest

from app.tools.text_tools import normalize_learning_topic


def test_normalize_learning_topic_trims_and_collapses_whitespace():
    result = normalize_learning_topic.invoke(
        {"topic": "  graph   machine learning  "}
    )

    assert result == "graph machine learning"


def test_normalize_learning_topic_rejects_blank_input():
    with pytest.raises(ValueError, match="topic cannot be empty"):
        normalize_learning_topic.invoke({"topic": "   "})


def test_normalize_learning_topic_exposes_specific_name_and_description():
    assert normalize_learning_topic.name == "normalize_learning_topic"
    assert "Normalize a single learning topic" in normalize_learning_topic.description
