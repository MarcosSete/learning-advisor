import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.base import BaseLLM


class FakeLLM(BaseLLM):
    def invoke(self, prompt: str) -> str:
        return """
        {
            "goal": "learn deep learning",
            "experience_level": "beginner",
            "mathematics_background": "weak in mathematics",
            "constraints": [
                "knows Python",
                "knows linear algebra"
            ]
        }
        """


def test_learning_advisor_interprets_learning_request():
    advisor = LearningAdvisor(FakeLLM())

    result = advisor.run(
        "I am a beginner who wants to learn deep learning. "
        "I know Python and linear algebra, but I am weak in mathematics."
    )

    assert result.goal == "learn deep learning"
    assert result.experience_level == "beginner"
    assert result.mathematics_background == "weak in mathematics"
    assert "knows Python" in result.constraints
    assert "knows linear algebra" in result.constraints


def test_learning_advisor_rejects_empty_request():
    advisor = LearningAdvisor(FakeLLM())

    with pytest.raises(ValueError):
        advisor.run("")
