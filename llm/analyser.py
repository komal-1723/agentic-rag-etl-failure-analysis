"""
analyzer.py

Coordinates the complete ETL Root Cause Analysis pipeline.

Flow

Current Error
        ↓
Retrieve Similar Incidents
        ↓
Retrieve Runbook
        ↓
Build Prompt
        ↓
Llama 3
        ↓
Return Structured Result
"""

from rag.retrieval import (
    retrieve_similar_incidents,
    retrieve_runbook,
    format_incident_results,
    format_runbook_results
)

from llm.prompt_builder import PromptBuilder
from llm.ollama_client import OllamaClient


class RCAAnalyzer:

    def __init__(self):
        self.client = OllamaClient()

    def analyze(self, error_text):

        print("\n" + "=" * 70)
        print("STARTING ROOT CAUSE ANALYSIS")
        print("=" * 70)

        print("\nRetrieving similar incidents...")

        incident_results = retrieve_similar_incidents(
            error_text
        )

        incidents = format_incident_results(
            incident_results
        )

        print(f"Retrieved {len(incidents)} incident(s).")

        print("\nRetrieving runbook...")

        runbook_results = retrieve_runbook(
            error_text
        )

        runbooks = format_runbook_results(
            runbook_results
        )

        print(f"Retrieved {len(runbooks)} runbook(s).")

        # -----------------------------------------
        # Convert incidents for Prompt Builder
        # -----------------------------------------

        prompt_incidents = []

        for incident in incidents:

            prompt_incidents.append(
                {
                    "category": incident.get("category", "Unknown"),
                    "error": incident.get("error", ""),
                    "root_cause": incident.get("cause", ""),
                    "solution": incident.get("fix", "")
                }
            )

        # -----------------------------------------
        # Convert runbook
        # -----------------------------------------

        if runbooks:

            runbook = {
                "title": "Retrieved Runbook",
                "category": runbooks[0].get("category", "Unknown"),
                "content": runbooks[0].get("content", "")
            }

        else:

            runbook = {}

        # -----------------------------------------
        # Build Prompt
        # -----------------------------------------

        builder = PromptBuilder(
            current_error=error_text,
            incidents=prompt_incidents,
            runbook=runbook
        )

        prompt = builder.build()

        print("\nSending prompt to Llama3...\n")

        analysis = self.client.generate(
            prompt
        )

        print("Analysis completed successfully.")

        # -----------------------------------------
        # Return structured result
        # -----------------------------------------

        result = {

            "error": error_text,

            "incidents": incidents,

            "runbook": runbook,

            "analysis": analysis

        }

        return result


if __name__ == "__main__":

    analyzer = RCAAnalyzer()

    result = analyzer.analyze(
        "Unable to connect to database"
    )

    print("\n" + "=" * 70)
    print("CURRENT ERROR")
    print("=" * 70)
    print(result["error"])

    print("\n" + "=" * 70)
    print("SIMILAR INCIDENTS")
    print("=" * 70)

    for incident in result["incidents"]:

        print(incident)

    print("\n" + "=" * 70)
    print("RUNBOOK")
    print("=" * 70)

    print(result["runbook"])

    print("\n" + "=" * 70)
    print("LLM ANALYSIS")
    print("=" * 70)

    print(result["analysis"])