from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.base import BaseLLM
from app.application.learning_presenter import LearningAdvisorPresenter


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


def test_presenter_confirms_understood_request():
    result = LearningAdvisor(FakeLLM()).run(
        "I want to learn deep learning from a book."
    )

    message = LearningAdvisorPresenter().present(result)

    assert "Request understood." in message
    assert "deep learning" in message
    assert "recommendation stage" in message
    assert "have not selected a resource yet" in message


def test_presenter_asks_for_missing_information():
    result = LearningAdvisor(FakeLLM()).run(
        "I want to learn from a book."
    )

    message = LearningAdvisorPresenter().present(result)

    assert "more information" in message
    assert "subject or topic" in message


def test_presenter_handles_empty_missing_information_gracefully():
    result = LearningAdvisor(FakeLLM()).run(
        "I want to learn deep learning from a book."
    )
    result.action = "clarify"
    result.missing_information = []

    message = LearningAdvisorPresenter().present(result)

    assert "proceed accurately" in message
    assert "more detail" in message
