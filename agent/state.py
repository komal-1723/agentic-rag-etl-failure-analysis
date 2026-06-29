"""
state.py

Shared state for the Agentic RAG workflow.

Each LangGraph node receives this state,
updates it, and passes it to the next node.
"""

from typing import TypedDict, List, Dict


class AgentState(TypedDict):

    # Current ETL error
    error: str

    # Retrieved historical incidents
    incidents: List[Dict]

    # Retrieved runbook
    runbook: Dict

    # Pipeline history
    history: List[Dict]

    # LLM analysis
    analysis: str

    # Verification confidence
    confidence: str

    # Generated PDF path
    pdf_path: str