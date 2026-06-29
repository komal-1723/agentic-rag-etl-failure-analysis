"""
tools.py

LangGraph Tools

These tools wrap the existing project functionality.

Nothing is reimplemented here.
The tools simply call the code you already built.

Project:
Agentic RAG ETL Failure Analysis

Author:
Komal K
"""

from parser.log_parser import parse_latest_error

from rag.retrieval import (
    retrieve_similar_incidents,
    retrieve_runbook,
    format_incident_results,
    format_runbook_results
)

from db.database import (
    fetch_all_incidents
)


# ==========================================================
# Tool 1
# Latest ETL Error
# ==========================================================

def latest_error_tool():

    """
    Reads the latest ETL error
    from pipeline.log.
    """

    error = parse_latest_error(
        "logs/pipeline.log"
    )

    return error


# ==========================================================
# Tool 2
# Similar Incident Retrieval
# ==========================================================

def incident_tool(
        error_text
):

    """
    Retrieves similar historical incidents.
    """

    results = retrieve_similar_incidents(
        error_text
    )

    incidents = format_incident_results(
        results
    )

    return incidents


# ==========================================================
# Tool 3
# Runbook Retrieval
# ==========================================================

def runbook_tool(
        error_text
):

    """
    Retrieves the most relevant runbook.
    """

    results = retrieve_runbook(
        error_text
    )

    runbooks = format_runbook_results(
        results
    )

    if runbooks:

        return {

            "title":
                "Retrieved Runbook",

            "category":
                runbooks[0].get(
                    "category",
                    "Unknown"
                ),

            "content":
                runbooks[0].get(
                    "content",
                    ""
                )

        }

    return {}


# ==========================================================
# Tool 4
# Pipeline History
# ==========================================================

def history_tool():

    """
    Retrieves pipeline history
    from SQLite.
    """

    rows = fetch_all_incidents()

    history = []

    for row in rows:

        history.append(

            {

                "id":
                    row["id"],

                "error":
                    row["error"],

                "category":
                    row["category"],

                "cause":
                    row["cause"],

                "fix":
                    row["fix"],

                "status":
                    row["status"]

            }

        )

    return history


# ==========================================================
# Tool Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("LANGGRAPH TOOLS TEST")
    print("=" * 70)

    error = latest_error_tool()

    print("\nLatest Error\n")
    print(error)

    print("\n")

    incidents = incident_tool(
        error
    )

    print("Incidents Retrieved\n")

    for incident in incidents:

        print(incident)

    print("\n")

    runbook = runbook_tool(
        error
    )

    print("Runbook\n")
    print(runbook)

    print("\n")

    history = history_tool()

    print("Pipeline History")

    print(f"\nTotal Runs : {len(history)}")