import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.base import BaseLLM


class FakeLLM(BaseLLM):
    def __init__(self, response: str):
        self.response = response

    def invoke(self, prompt: str) -> str:
        return self.response


def learning_request_response() -> str:
    return """
    {
        "goal": "learn deep learning",
        "topics": ["deep learning"],
        "resource_type": "book",
        "experience_level": "beginner",
        "mathematics_background": "weak in mathematics",
        "constraints": [
            "knows Python",
            "knows linear algebra"
        ]
    }
    """


def test_learning_advisor_interprets_learning_request():
    advisor = LearningAdvisor(FakeLLM(learning_request_response()))

    result = advisor.interpret(
        "I am a beginner who wants to learn deep learning from a book. "
        "I know Python and linear algebra, but I am weak in mathematics."
    )

    assert result.goal == "learn deep learning"
    assert result.topics == ["deep learning"]
    assert result.resource_type == "book"
    assert result.experience_level == "beginner"
    assert result.mathematics_background == "weak in mathematics"
    assert "knows Python" in result.constraints
    assert "knows linear algebra" in result.constraints


def test_learning_advisor_decides_to_recommend():
    advisor = LearningAdvisor(FakeLLM(learning_request_response()))

    result = advisor.run(
        "I want a book to learn deep learning."
    )

    assert result.action == "recommend"
    assert result.missing_information == []


def test_learning_advisor_decides_to_clarify_when_topic_is_missing():
    response = """
    {
        "goal": "learn something new",
        "topics": [],
        "resource_type": "either",
        "experience_level": null,
        "mathematics_background": null,
        "constraints": []
    }
    """
    advisor = LearningAdvisor(FakeLLM(response))

    result = advisor.run("I want to learn something new.")

    assert result.action == "clarify"
    assert "subject or topic" in result.missing_information


def test_learning_advisor_rejects_empty_request():
    advisor = LearningAdvisor(FakeLLM(learning_request_response()))

    with pytest.raises(ValueError):
        advisor.run("")
