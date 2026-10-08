from app.agent.learning_advisor import LearningAdvisor
from app.domain.learning import LearningResult


class LearningAdvisorService:
    """Application service that exposes the learning-advisor use case."""

    def __init__(self, advisor: LearningAdvisor) -> None:
        self.advisor = advisor

    def analyze_request(self, user_input: str) -> LearningResult:
        """Analyze a learning request through the agent."""
        return self.advisor.run(user_input)
