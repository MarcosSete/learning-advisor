import pytest

from app.agent.learning_advisor import LearningAdvisor


def test_learning_advisor_accepts_request():
    advisor = LearningAdvisor()

    result = advisor.run(
        "Quero aprender Deep Learning."
    )

    assert result == "Quero aprender Deep Learning."


def test_learning_advisor_rejects_empty_request():
    advisor = LearningAdvisor()

    with pytest.raises(ValueError):
        advisor.run("")