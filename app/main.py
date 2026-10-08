import argparse
import json

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM
from app.application.learning_service import LearningAdvisorService


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Learning Advisor agent"
    )
    parser.add_argument(
        "request",
        help="Learning request to analyze",
    )
    args = parser.parse_args()

    advisor = LearningAdvisor(DeepSeekLLM())
    service = LearningAdvisorService(advisor)
    result = service.analyze_request(args.request)

    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
