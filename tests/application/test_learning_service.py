from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.base import BaseLLM
from app.application.learning_service import LearningAdvisorService


class FakeLLM(BaseLLM):
    def invoke(self, prompt: str) -> str:
        return """
        {
            "goal": "learn deep learning",
            "topics": ["deep learning"],
            "resource_type": "book",
            "experience_level": "beginner",
            "mathematics_background": null,
            "constraints": []
        }
        """


def test_learning_service_exposes_agent_use_case():
    service = LearningAdvisorService(LearningAdvisor(FakeLLM()))

    result = service.analyze_request("I want to learn deep learning from a book.")

    assert result.action == "recommend"
    assert result.intent.topics == ["deep learning"]
    assert result.intent.resource_type == "book"
