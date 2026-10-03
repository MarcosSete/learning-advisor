import sys

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM


def create_learning_advisor() -> LearningAdvisor:
    """Build the application using the configured model adapter."""
    return LearningAdvisor(DeepSeekLLM())


def main() -> int:
    """Run the Learning Advisor from the command line."""
    user_input = " ".join(sys.argv[1:]).strip()

    if not user_input:
        print('Usage: python -m app "your learning request"')
        return 1

    advisor = create_learning_advisor()
    intent = advisor.run(user_input)

    print(intent.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
