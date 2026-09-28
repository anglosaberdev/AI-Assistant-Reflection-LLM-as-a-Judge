
import os
from dotenv import load_dotenv

import streamlit as st

from app.ai_assistant import AIAssistant


# Configure the Streamlit page
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖"
)

# Display the application title
st.title("🤖 AI Assistant")


# Load environment variables from the .env file
load_dotenv()

# Get the Hugging Face API token
api_key = os.getenv(
    "HUGGINGFACEHUB_API_TOKEN"
)

# Check if the API token is available
if not api_key:

    st.error(
        "HUGGINGFACEHUB_API_TOKEN is not set."
    )

    st.stop()


# Create the AI Assistant
assistant = AIAssistant(
    api_key
)


# Get the user's prompt
prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Ask me anything..."
)


# Generate a response when the user clicks the button
if st.button("Generate"):

    # Validate the user input
    if not prompt.strip():

        st.warning(
            "Please enter a prompt."
        )

    else:

        # Execute the AI Assistant workflow
        with st.spinner("Generating..."):

            result = assistant.invoke(prompt)

        # Get the final AI response
        response = result["messages"][-1]

        # Display the AI response
        st.subheader("AI Response")

        st.write(
            response.content
        )

        # Display the reflection feedback
        if "feedback" in result:

            st.subheader("Reflection Feedback")

            st.write(
                result["feedback"]
            )

        # Display the evaluation result
        if "evaluation" in result:

            st.subheader("Evaluation")

            st.write(
                result["evaluation"]
            )

