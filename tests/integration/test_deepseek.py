import pytest

from app.agent.models.deepseek import DeepSeekLLM
from app.infrastructure.config.settings import get_settings
from app.agent.learning_advisor import LearningAdvisor

@pytest.mark.integration
def test_deepseek_connection():
    settings = get_settings()

    if not settings.deepseek_api_key:
        pytest.skip("DEEPSEEK_API_KEY is not configured.")

    deepseek_model = DeepSeekLLM()
    agent = LearningAdvisor(deepseek_model)

    response = agent.run(
        "Respond only with: DeepSeek integration is working."
    )



    assert response
    assert isinstance(response, str)
    assert len(response.strip()) > 0