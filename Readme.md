# 🤖 AI Assistant — Reflection & LLM-as-a-Judge

A simple AI Assistant built with **Python, LangChain, LangGraph, and Hugging Face**.

This project demonstrates how to build an AI application using a structured workflow instead of calling an LLM directly from the UI.

The assistant follows a simple pipeline:

```text
User Prompt
    ↓
Generator
    ↓
AI Response
    ↓
Reflector
    ↓
Feedback
    ↓
Evaluator
    ↓
PASS / FAIL
```

---

## 🎯 Project Goal

The goal of this project is to demonstrate a clean and modular approach to building an AI application with:

* LLM abstraction
* Response generation
* Reflection
* LLM-as-a-Judge evaluation
* State management
* Workflow orchestration with LangGraph
* Streamlit UI

The project separates each responsibility into its own component.

---

## 🏗️ Architecture

```text
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Streamlit   │
                    │      UI      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AIAssistant  │
                    │ Orchestrator │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Generate   │
                    │   Generator  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AI Response  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Reflection  │
                    │   Reflector  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Feedback   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Evaluation  │
                    │ LLM-as-Judge │
                    └──────┬───────┘
                           │
                      ┌────┴────┐
                      │         │
                    PASS       FAIL
```

---

## 🧩 Main Components

### 1. `LLMService`

Responsible for creating and configuring the Hugging Face LLM.

It centralizes:

* Model configuration
* API authentication
* Temperature
* Maximum generated tokens

This keeps LLM configuration separate from the application logic.

---

### 2. `Generator`

The `Generator` is responsible only for generating the AI response.

```text
Messages
   ↓
Generator
   ↓
AIMessage
```

It does not handle evaluation or reflection.

This separation makes the component easier to test and reuse.

---

### 3. `Reflector`

The `Reflector` reviews the generated AI response.

It looks for:

* Incorrect information
* Missing information
* Lack of clarity
* Relevance issues
* Possible improvements

The Reflector does **not directly modify the AI response**.

Instead, it produces feedback that can later be used to improve the response.

```text
AIMessage
   ↓
Reflector
   ↓
Feedback
```

---

### 4. `Evaluator`

The `Evaluator` implements the **LLM-as-a-Judge** pattern.

Instead of manually checking the response, another LLM call evaluates the generated answer.

It checks:

* Correctness
* Relevance
* Clarity
* Completeness

The current implementation returns:

```text
PASS
```

or:

```text
FAIL
```

This creates a simple quality gate for the AI response.

```text
AIMessage
   ↓
LLM-as-a-Judge
   ↓
PASS / FAIL
```

---

### 5. `AssistantState`

The application state is represented using a `TypedDict`.

```python
class AssistantState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    feedback: str

    evaluation: str
```

The state allows different nodes in the LangGraph workflow to share information.

For example:

```text
messages
   ↓
Generator
   ↓
messages + AIMessage
   ↓
Reflector
   ↓
feedback
   ↓
Evaluator
   ↓
evaluation
```

---

### 6. `AIAssistant`

`AIAssistant` acts as the application orchestrator.

It connects:

* Generator
* Reflector
* Evaluator
* AssistantState
* LangGraph

The business logic is therefore separated from the Streamlit interface.

---

## 🔄 Current Workflow

The current LangGraph workflow is:

```text
START
  ↓
Generate
  ↓
Reflection
  ↓
Evaluation
  ↓
END
```

### Generate

The Generator creates the initial AI response.

### Reflection

The Reflector reviews the latest AI response and generates improvement feedback.

### Evaluation

The Evaluator uses the LLM-as-a-Judge approach to determine whether the response passes the quality checks.

---

## 🧠 Reflection vs Evaluation

These two components have different responsibilities.

### Reflection

Answers:

> What can be improved?

Example:

```text
The response is missing an explanation of the main concept.
```

### Evaluation

Answers:

> Is the response good enough?

Example:

```text
FAIL
```

Together:

```text
Generate
   ↓
Reflect
   ↓
Identify Problems
   ↓
Evaluate
   ↓
PASS / FAIL
```

---

## 🛠️ Technologies

* **Python**
* **LangChain**
* **LangGraph**
* **Hugging Face**
* **Streamlit**
* **python-dotenv**

---

## 📁 Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── ai_assistant.py
    ├── evaluator.py
    ├── generator.py
    ├── reflector.py
    ├── state.py
    └── llm_service.py
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Hugging Face

Create a `.env` file:

```env
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Do not commit the `.env` file to GitHub.

---

## ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

Then open the Streamlit application in your browser.

---

## 🚀 Future Improvements

The current project intentionally keeps the workflow simple.

The next evolution is to introduce **conditional routing and iterative reflection**:

```text
             Generate
                ↓
             Evaluate
                ↓
          ┌─────┴─────┐
          │           │
        PASS         FAIL
          │           │
          ▼           ▼
         END       Reflect
                      ↓
                   Generate
                      ↓
                   Evaluate
```

This will allow the system to automatically improve an AI response when the evaluator determines that it does not meet the required quality criteria.

Future improvements may include:

* Conditional LangGraph routing
* Reflection → Generation loop
* Maximum retry / iteration limit
* Structured evaluation output
* Evaluation scores
* Better prompt templates
* Observability and tracing
* Production evaluation frameworks
* Automated test datasets
* Human-in-the-loop evaluation

---

## 💡 What This Project Demonstrates

This project demonstrates an important AI Engineering principle:

> **An AI application is more than an LLM call.**

A production-oriented AI system needs clear separation between:

```text
LLM
 ↓
Generation
 ↓
Reflection
 ↓
Evaluation
 ↓
Workflow
 ↓
Application
```

The project uses **LangChain for LLM interaction** and **LangGraph for workflow orchestration**, making it easier to extend the system with additional nodes, tools, routing logic, and iterative AI workflows.

---

## 👨‍💻 Author

**Angelo Saber**

AI / Generative AI Engineer

GitHub: `Eng.AngeloSaber`
