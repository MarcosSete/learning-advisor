from typing import Literal

from pydantic import BaseModel, Field


class LearningIntent(BaseModel):
    """Structured representation of a user's learning request."""

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
