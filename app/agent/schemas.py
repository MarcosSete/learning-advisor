from pydantic import BaseModel, Field


class LearningIntent(BaseModel):
    """Structured representation of a user's learning request."""

    goal: str = Field(
        description="What the user wants to learn or achieve."
    )
    constraints: list[str] = Field(
        default_factory=list,
        description="Relevant constraints expressed by the user.",
    )
