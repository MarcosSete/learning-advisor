import argparse

from app.application.learning_presenter import LearningAdvisorPresenter
from app.infrastructure.factories import create_learning_advisor_service


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Learning Advisor agent"
    )
    parser.add_argument(
        "request",
        help="Learning request to analyze",
    )
    args = parser.parse_args()

    service = create_learning_advisor_service()
    result = service.analyze_request(args.request)

    print(LearningAdvisorPresenter().present(result))
