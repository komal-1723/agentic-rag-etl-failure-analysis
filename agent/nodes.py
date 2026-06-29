"""
nodes.py

LangGraph Nodes

Each node performs ONE responsibility.

Flow

Read Error
      ↓
Retrieve Incidents
      ↓
Retrieve Runbook
      ↓
Generate RCA
      ↓
Verify Analysis
"""

from agent.tools import (
    latest_error_tool,
    incident_tool,
    runbook_tool,
    history_tool
)

from agent.state import AgentState

from llm.analyser import RCAAnalyzer


# ==========================================================
# Node 1
# Read Latest ETL Error
# ==========================================================

def read_error_node(
        state: AgentState
):

    print("\nReading latest ETL error...")

    error = latest_error_tool()

    state["error"] = error

    return state


# ==========================================================
# Node 2
# Retrieve Similar Incidents
# ==========================================================

def retrieve_incidents_node(
        state: AgentState
):

    print("\nRetrieving historical incidents...")

    incidents = incident_tool(
        state["error"]
    )

    state["incidents"] = incidents

    return state


# ==========================================================
# Node 3
# Retrieve Runbook
# ==========================================================

def retrieve_runbook_node(
        state: AgentState
):

    print("\nRetrieving troubleshooting runbook...")

    runbook = runbook_tool(
        state["error"]
    )

    state["runbook"] = runbook

    return state


# ==========================================================
# Node 4
# Generate Root Cause Analysis
# ==========================================================

def generate_rca_node(
        state: AgentState
):

    print("\nGenerating Root Cause Analysis...")

    analyzer = RCAAnalyzer()

    result = analyzer.analyze(
        state["error"],
        state["incidents"],
        state["runbook"]
    )

    state["analysis"] = result["analysis"]

    return state


# ==========================================================
# Node 5
# Verify RCA
# ==========================================================

def verify_rca_node(
        state: AgentState
):

    print("\nVerifying RCA...")

    incidents = state.get(
        "incidents",
        []
    )

    runbook = state.get(
        "runbook",
        {}
    )

    analysis = state.get(
        "analysis",
        ""
    )

    confidence = "Low"

    if incidents:

        confidence = "Medium"

    if incidents and runbook:

        confidence = "High"

    if len(analysis) > 100:

        confidence = "Very High"

    state["confidence"] = confidence

    return state


# ==========================================================
# Node 6
# Retrieve Pipeline History
# ==========================================================

def retrieve_history_node(
        state: AgentState
):

    print("\nRetrieving pipeline history...")

    history = history_tool()

    state["history"] = history

    return state


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    state = {

        "error": "",

        "incidents": [],

        "runbook": {},

        "analysis": "",

        "confidence": "",

        "history": [],
         
        "analysis": "",

        "confidence": "",

        "pdf_path": ""

    }

    state = read_error_node(state)

    state = retrieve_incidents_node(state)

    state = retrieve_runbook_node(state)

    state = retrieve_history_node(state)

    state = generate_rca_node(state)

    state = verify_rca_node(state)

    print("\n")
    print("=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    print(state)