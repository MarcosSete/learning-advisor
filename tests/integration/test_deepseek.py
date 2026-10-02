import pytest

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM
from app.infrastructure.config.settings import get_settings


@pytest.mark.integration
def test_deepseek_connection():
    settings = get_settings()

    if not settings.deepseek_api_key:
        pytest.skip("DEEPSEEK_API_KEY is not configured.")

    advisor = LearningAdvisor(DeepSeekLLM())

    result = advisor.run(
        "I want to learn deep learning. "
        "I already know Python and linear algebra."
    )

    assert result.goal
    assert result.constraints
