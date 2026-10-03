from app.agent.models.base import BaseLLM
from app.agent.schemas import LearningIntent


class LearningAdvisor:
    """Interpret learning requests for the Learning Advisor system."""

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
2. The user's experience level, when stated.
3. The user's mathematics background or difficulty, when stated.
4. Other relevant constraints.

Use null when a field is not supported by the request.
Do not invent user characteristics.

Return only valid JSON using this structure:

{{
    "goal": "string",
    "experience_level": "string or null",
    "mathematics_background": "string or null",
    "constraints": ["string"]
}}

User request:
{user_input}
"""

        response = self.model.invoke(prompt)
        return LearningIntent.model_validate_json(response)

    def run(self, user_input: str) -> LearningIntent:
        """Interpret the user's learning request."""
        return self.interpret(user_input)
