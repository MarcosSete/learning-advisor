from app.domain.learning import LearningResult


class LearningAdvisorPresenter:
    """Format learning-advisor results for a text-based user experience."""

    def present(self, result: LearningResult) -> str:
        if result.action == "clarify":
            return self._clarification_message(result)

        return self._ready_message(result)

    @staticmethod
    def _clarification_message(result: LearningResult) -> str:
        if not result.missing_information:
            return (
                "I need a bit more information to proceed accurately. "
                "Please provide more detail about your learning request."
            )

        missing = ", ".join(result.missing_information)
        return (
            "I need a bit more information to proceed accurately. "
            f"Please provide: {missing}."
        )

    @staticmethod
    def _ready_message(result: LearningResult) -> str:
        topics = ", ".join(result.intent.topics)
        return (
            f"Request understood. Goal: {result.intent.goal}. "
            f"Topic: {topics}. "
            "The request is ready for the recommendation stage."
        )
