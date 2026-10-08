import argparse
import json

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

    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
