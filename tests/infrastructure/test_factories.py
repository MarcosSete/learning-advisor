from app.agent.models.base import BaseLLM
from app.infrastructure import factories


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


def test_create_learning_advisor_service_composes_dependencies(monkeypatch):
    monkeypatch.setattr(factories, "DeepSeekLLM", lambda: FakeLLM())

    service = factories.create_learning_advisor_service()
    result = service.analyze_request(
        "I want to learn deep learning from a book."
    )

    assert result.action == "recommend"
    assert result.intent.topics == ["deep learning"]
