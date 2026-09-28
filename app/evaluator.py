from typing import Sequence

from langchain_core.messages import BaseMessage


class Evaluator:
    """
    Responsible for evaluating the generated AI response
    using an LLM as a judge.
    """

    def __init__(self, llm):
        # Store the configured LLM
        self.llm = llm

    def evaluate(
        self,
        messages: Sequence[BaseMessage]
    ) -> str:

        # Create a prompt for the LLM judge
        evaluation_prompt = f"""
        Evaluate the following AI response.

        Decide whether the response is good enough.

        Check:
        - Correctness
        - Relevance
        - Clarity
        - Completeness

        Response:
        {messages}

        Return only:
        PASS
        or
        FAIL
        """

        # Ask the LLM to evaluate the response
        response = self.llm.invoke(
            evaluation_prompt
        )

        # Return the evaluation result
        return response.content.strip()
