from app.agent.decision import LearningDecision
from app.agent.models.base import BaseLLM
from app.agent.schemas import LearningIntent


class LearningAdvisor:
    """Interpret learning requests and decide the next action."""

    name = "LearningAdvisor"

    def __init__(self, model: BaseLLM) -> None:
        self.model = model

    def interpret(self, user_input: str) -> LearningIntent:
        """Convert an unstructured learning request into a typed intent."""
        if not user_input.strip():
            raise ValueError("user_input cannot be empty")

        prompt = f"""
Analyze the following learning request.

Extract only information explicitly stated or directly implied by the user:
1. The main learning goal.
2. The requested subject or topics.
3. Whether the user prefers a book, course notes, or either.
4. The user's experience level, when stated.
5. The user's mathematics background or difficulty, when stated.
6. Other relevant constraints.

For resource_type, use exactly one of:
- "book"
- "course_notes"
- "either"

Use an empty list when no specific topic or constraint is stated.
Use null when a learner attribute is not supported by the request.
Do not invent user characteristics.

Return only valid JSON using this structure:

{{
    "goal": "string",
    "topics": ["string"],
    "resource_type": "book | course_notes | either",
    "experience_level": "string or null",
    "mathematics_background": "string or null",
    "constraints": ["string"]
}}

User request:
{user_input}
"""

        response = self.model.invoke(prompt)
        return LearningIntent.model_validate_json(response)

    def decide(self, intent: LearningIntent) -> LearningDecision:
        """Decide whether the request is ready for recommendation."""
        missing_information: list[str] = []

        if not intent.goal.strip():
            missing_information.append("learning goal")

        if not intent.topics:
            missing_information.append("subject or topic")

        if missing_information:
            return LearningDecision(
                action="clarify",
                missing_information=missing_information,
            )

        return LearningDecision(action="recommend")

    def run(self, user_input: str) -> LearningDecision:
        """Interpret the request and decide the next action."""
        intent = self.interpret(user_input)
        return self.decide(intent)
