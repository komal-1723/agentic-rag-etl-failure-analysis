"""
graph.py

Builds the LangGraph workflow.

Workflow

Read Error
      ↓
Retrieve Incidents
      ↓
Retrieve Runbook
      ↓
Retrieve History
      ↓
Generate RCA
      ↓
Verify RCA
"""

from langgraph.graph import StateGraph
from langgraph.graph import END

from agent.state import AgentState

from agent.nodes import (
    read_error_node,
    retrieve_incidents_node,
    retrieve_runbook_node,
    retrieve_history_node,
    generate_rca_node,
    verify_rca_node
)


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(AgentState)

builder.add_node(
    "read_error",
    read_error_node
)

builder.add_node(
    "retrieve_incidents",
    retrieve_incidents_node
)

builder.add_node(
    "retrieve_runbook",
    retrieve_runbook_node
)

builder.add_node(
    "retrieve_history",
    retrieve_history_node
)

builder.add_node(
    "generate_rca",
    generate_rca_node
)

builder.add_node(
    "verify_rca",
    verify_rca_node)


# ==========================================================
# Entry Point
# ==========================================================

builder.set_entry_point(
    "read_error"
)


# ==========================================================
# Edges
# ==========================================================

builder.add_edge(
    "read_error",
    "retrieve_incidents"
)

builder.add_edge(
    "retrieve_incidents",
    "retrieve_runbook"
)

builder.add_edge(
    "retrieve_runbook",
    "retrieve_history"
)

builder.add_edge(
    "retrieve_history",
    "generate_rca"
)

builder.add_edge(
    "generate_rca",
    "verify_rca"
)

builder.add_edge(
    "verify_rca",
    END
)


# ==========================================================
# Compile
# ==========================================================

graph = builder.compile()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    initial_state = {

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

    result = graph.invoke(
        initial_state
    )

    print("\n")
    print("=" * 70)
    print("FINAL AGENT STATE")
    print("=" * 70)

    print("\nError")
    print(result["error"])

    print("\nIncidents")
    print(len(result["incidents"]))

    print("\nRunbook")
    print(result["runbook"])

    print("\nHistory")
    print(len(result["history"]))

    print("\nConfidence")
    print(result["confidence"])

    print("\nAnalysis")
    print(result["analysis"])