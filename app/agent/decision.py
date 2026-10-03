from typing import Literal

from pydantic import BaseModel, Field


class LearningDecision(BaseModel):
    """Decision about the next action for a learning request."""

    action: Literal["recommend", "clarify"] = Field(
        description="Next action the Learning Advisor should take."
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description="Information needed before making a recommendation.",
    )
