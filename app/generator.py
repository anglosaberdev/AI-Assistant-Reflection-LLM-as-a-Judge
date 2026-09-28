
from typing import Sequence

from langchain_core.messages import BaseMessage

from .llm_service import LLMService


class Generator:
    """
    Responsible for generating responses from the LLM.
    """

    def __init__(self, llm_service: LLMService):

        self.llm = llm_service.get_llm()

    def generate(
        self,
        messages: Sequence[BaseMessage]
    ):

        response = self.llm.invoke(messages)

        return response
