from typing import Literal

from pydantic import BaseModel, Field


class LearningIntent(BaseModel):
    """Domain representation of a user's learning request."""

    goal: str = Field(
        description="What the user wants to learn or achieve."
    )
    topics: list[str] = Field(
        default_factory=list,
        description="Subjects or topics explicitly requested by the user.",
    )
    resource_type: Literal["book", "course_notes", "either"] = Field(
        default="either",
        description="Preferred type of learning resource.",
    )
    experience_level: str | None = Field(
        default=None,
        description="The user's stated experience level with the subject.",
    )
    mathematics_background: str | None = Field(
        default=None,
        description="The user's stated mathematics background or difficulty.",
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Relevant constraints expressed by the user.",
    )


class LearningDecision(BaseModel):
    """Domain decision about the next action for a learning request."""

    action: Literal["recommend", "clarify"] = Field(
        description="Next action the Learning Advisor should take."
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description="Information needed before making a recommendation.",
    )


class LearningResult(BaseModel):
    """Domain result of interpreting a request and deciding the next action."""

    intent: LearningIntent
    action: Literal["recommend", "clarify"]
    missing_information: list[str] = Field(default_factory=list)
