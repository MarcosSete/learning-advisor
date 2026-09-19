class LearningAdvisor:
    """
    Main agent of the Learning Advisor system.

    Responsible for interpreting learning requests
    and coordinating the recommendation process.
    """

    name = "LearningAdvisor"

    def run(self, user_input: str) -> str:
        if not user_input.strip():
            raise ValueError("user_input cannot be empty")

        return user_input