
from typing import Sequence

from langchain_core.messages import BaseMessage


class Reflector:
    """
    Responsible for reviewing the generated response
    and providing feedback for improvement.
    """

    def __init__(self, llm):
        # Store the configured LLM
        self.llm = llm

    def reflect(
        self,
        messages: Sequence[BaseMessage]
    ) -> str:

        # Create a prompt that asks the LLM to review the response
        reflection_prompt = f"""
        Review the following conversation and response.

        Your task is to identify:
        - Incorrect information
        - Missing information
        - Lack of clarity
        - Relevance issues
        - Possible improvements

        Conversation:
        {messages}

        Provide clear and concise feedback for improving the response.
        """

        # Send the reflection prompt to the LLM
        response = self.llm.invoke(
            reflection_prompt
        )

        # Return the feedback as plain text
        return response.content
