import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM
from app.agent.schemas import LearningIntent
from app.infrastructure.config.settings import get_settings


@pytest.mark.integration
def test_learning_advisor_with_deepseek():
    settings = get_settings()

    if not settings.deepseek_api_key:
        pytest.skip("DEEPSEEK_API_KEY is not configured.")

    advisor = LearningAdvisor(DeepSeekLLM())

    result = advisor.run(
        "Quero aprender Deep Learning. Já conheço Python e álgebra linear."
    )

    assert isinstance(result, LearningIntent)
    assert result.goal
    assert isinstance(result.constraints, list)
