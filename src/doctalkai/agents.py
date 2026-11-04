# =========================
# Import Libraries
# =========================

from deepagents import create_deep_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from doctalkai.prompts import (
    RAG_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
    CHUNK_ANALYST_INSTRUCTIONS
)
from doctalkai.tools import search_documentation, backend


# =========================
# Agent Configuration
# =========================

max_concurrent_analysts = 3

INSTRUCTIONS = (
    RAG_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_analysts=max_concurrent_analysts
    )
)


# =========================
# Chunk Analyst Subagent
# =========================

chunk_analyst_subagent = {
    "name": "chunk-analyst",
    "description": (
        "Analyse one retrieved documentation chunk file. "
        "Pass the user question and a single file path under /retrieved/."
    ),
    "system_prompt": CHUNK_ANALYST_INSTRUCTIONS
}


# =========================
# Initialize Groq Model
# =========================

model = ChatGroq(
    model="openai/gpt-oss-120b"
)


# =========================
# Create Main Agent
# =========================

agent = create_deep_agent(
    model=model,
    tools=[search_documentation],
    backend=backend,
    system_prompt=INSTRUCTIONS,
    subagents=[chunk_analyst_subagent]
)


# =========================
# Test Agent
# =========================

example_query = "What are the causes of climate change?"

result = agent.invoke(
    {"messages": [HumanMessage(content=example_query)]}
)

print(result["messages"][-1].content)