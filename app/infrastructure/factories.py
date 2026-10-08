from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM
from app.application.learning_service import LearningAdvisorService


def create_learning_advisor_service() -> LearningAdvisorService:
    """Compose the production dependencies for the learning-advisor use case."""
    model = DeepSeekLLM()
    advisor = LearningAdvisor(model)
    return LearningAdvisorService(advisor)
