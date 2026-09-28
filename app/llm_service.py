from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


class LLMService:
    """
    Responsible for creating and configuring
    the Hugging Face LLM used by our application.
    """

    def __init__(
        self,
        key: str,
        model_name: str = "Qwen/Qwen3-4B-Instruct-2507",
    ):
        # Store the Hugging Face API key
        self.key = key

        # Store the model name
        self.model_name = model_name

        # Initialize the LLM
        self.llm = self._init_llm()

    def _init_llm(self):
        """
        Create and return the Hugging Face Chat LLM.
        """

        endpoint = HuggingFaceEndpoint(
            repo_id=self.model_name,
            huggingfacehub_api_token=self.key,
            temperature=0.3,
            max_new_tokens=512,
        )

        return ChatHuggingFace(
            llm=endpoint
        )

    def get_llm(self):
        """
        Return the configured LLM.
        """

        return self.llm

