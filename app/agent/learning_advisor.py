class LearningAdvisor:
    """
    Main agent of the Learning Advisor system.

    Responsible for interpreting learning requests
    and coordinating the recommendation process.
    """

    from app.agent.models.base import BaseLLM

    name = "LearningAdvisor"

    def __init__(self, model: BaseLLM) -> None:
        self.model = model

    def run(self, user_input: str) -> str:
        if not user_input.strip():
            raise ValueError("user_input cannot be empty")

        return self.model.invoke(user_input)