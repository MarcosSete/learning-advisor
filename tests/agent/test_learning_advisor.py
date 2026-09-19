import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM


def test_learning_advisor_accepts_request():
    model = DeepSeekLLM()
    advisor = LearningAdvisor(model)

    result = advisor.run(
        "Quero aprender Deep Learning."
    )

    assert result == "Quero aprender Deep Learning."


def test_learning_advisor_rejects_empty_request():
    model = DeepSeekLLM()
    advisor = LearningAdvisor(model)

    with pytest.raises(ValueError):
        advisor.run("")