import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.base import BaseLLM


class FakeLLM(BaseLLM):
    def invoke(self, prompt: str) -> str:
        return """
        {
            "goal": "learn deep learning",
            "constraints": [
                "knows Python",
                "knows linear algebra"
            ]
        }
        """


def test_learning_advisor_interprets_learning_request():
    advisor = LearningAdvisor(FakeLLM())

    result = advisor.run(
        "I want to learn deep learning. "
        "I already know Python and linear algebra."
    )

    assert result.goal == "learn deep learning"
    assert "knows Python" in result.constraints
    assert "knows linear algebra" in result.constraints


def test_learning_advisor_rejects_empty_request():
    advisor = LearningAdvisor(FakeLLM())

    with pytest.raises(ValueError):
        advisor.run("")
