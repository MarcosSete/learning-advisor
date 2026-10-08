from app.domain.learning import LearningResult


class LearningAdvisorPresenter:
    """Format the learning-advisor result for a text-based user experience."""

    def present(self, result: LearningResult) -> str:
        if result.action == "clarify":
            return self._clarification_message(result)

        return self._ready_message(result)

    @staticmethod
    def _clarification_message(result: LearningResult) -> str:
        missing = ", ".join(result.missing_information)
        return (
            "I can help analyze your learning request, but I need "
            f"more information about: {missing}."
        )

    @staticmethod
    def _ready_message(result: LearningResult) -> str:
        topics = ", ".join(result.intent.topics)
        return (
            f"Request understood. Goal: {result.intent.goal}. "
            f"Topic: {topics}. "
            "The request is ready for the recommendation stage."
        )
