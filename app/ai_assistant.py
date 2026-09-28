from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from .generator import Generator
from .llm_service import LLMService
from .state import AssistantState
from .reflector import Reflector
from .evaluator import Evaluator


class AIAssistant:

    def __init__(self, key: str):

        # Create the LLM service
        llm_service = LLMService(key)

        # Create the Generator responsible for generating responses
        self.generator = Generator(
            llm_service
        )

        # Create the Reflector responsible for reviewing AI responses
        self.reflector = Reflector(
            llm_service.get_llm()
        )

        # Create the Evaluator responsible for judging AI responses
        self.evaluator = Evaluator(
            llm_service.get_llm()
        )

        # Build and compile the LangGraph workflow
        self.graph = self._build_graph()

    def _generate_node(
        self,
        state: AssistantState
    ) -> AssistantState:

        # Generate an AI response using the current messages
        response = self.generator.generate(
            state["messages"]
        )

        # Add the generated AI response to the messages
        return {
            "messages": [response]
        }

    def _reflection_node(
        self,
        state: AssistantState
    ) -> AssistantState:

        # Get the latest AI response
        ai_message = state["messages"][-1]

        # Ask the Reflector to review the AI response
        feedback = self.reflector.reflect(
            [ai_message]
        )

        # Store the reflection feedback in the state
        return {
            "feedback": feedback
        }

    def _evaluation_node(
        self,
        state: AssistantState
    ) -> AssistantState:

        # Get the latest AI response
        ai_message = state["messages"][-1]

        # Ask the Evaluator to judge the AI response
        evaluation = self.evaluator.evaluate(
            [ai_message]
        )

        # Store the evaluation result in the state
        return {
            "evaluation": evaluation
        }

    def _build_graph(self):

        # Create the LangGraph state graph
        builder = StateGraph(AssistantState)

        # Add the generation node
        builder.add_node(
            "generate",
            self._generate_node
        )

        # Add the reflection node
        builder.add_node(
            "reflection",
            self._reflection_node
        )

        # Add the evaluation node
        builder.add_node(
            "evaluation",
            self._evaluation_node
        )

        # START → generate
        builder.add_edge(
            START,
            "generate"
        )

        # generate → reflection
        builder.add_edge(
            "generate",
            "reflection"
        )

        # reflection → evaluation
        builder.add_edge(
            "reflection",
            "evaluation"
        )

        # evaluation → END
        builder.add_edge(
            "evaluation",
            END
        )

        # Compile the graph
        return builder.compile()

    def invoke(self, prompt: str):

        # Create the initial state with the user's message
        state: AssistantState = {
            "messages": [
                HumanMessage(content=prompt)
            ]
        }

        # Execute the graph
        return self.graph.invoke(state)