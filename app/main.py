import argparse
import json

from app.agent.learning_advisor import LearningAdvisor
from app.agent.models.deepseek import DeepSeekLLM


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
    result = advisor.run(args.request)

    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
