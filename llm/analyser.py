"""
analyser.py

RCA Analyzer

Receives the already retrieved context from LangGraph.

Flow

Current Error
        ↓
Historical Incidents
        ↓
Runbook
        ↓
Prompt Builder
        ↓
Llama 3
        ↓
Structured Result
"""

from llm.prompt_builder import PromptBuilder
from llm.ollama_client import OllamaClient


class RCAAnalyzer:

    def __init__(self):

        self.client = OllamaClient()

    def analyze(
        self,
        error_text,
        incidents,
        runbook
    ):

        print("\n" + "=" * 70)
        print("STARTING ROOT CAUSE ANALYSIS")
        print("=" * 70)

        print(f"\nUsing {len(incidents)} retrieved incident(s).")

        if runbook:

            print(
                f"Using runbook: "
                f"{runbook.get('category', 'Unknown')}"
            )

        else:

            print("No runbook retrieved.")

        # --------------------------------------------------
        # Convert incidents for Prompt Builder
        # --------------------------------------------------

        prompt_incidents = []

        for incident in incidents:

            prompt_incidents.append(

                {

                    "category":
                        incident.get(
                            "category",
                            "Unknown"
                        ),

                    "error":
                        incident.get(
                            "error",
                            ""
                        ),

                    "root_cause":
                        incident.get(
                            "cause",
                            ""
                        ),

                    "solution":
                        incident.get(
                            "fix",
                            ""
                        )

                }

            )

        # --------------------------------------------------
        # Convert runbook
        # --------------------------------------------------

        prompt_runbook = {}

        if runbook:

            content = runbook.get(
                "content",
                ""
            )

            if isinstance(content, str):

                steps = [

                    step.strip()

                    for step in content.split(".")

                    if step.strip()

                ]

            else:

                steps = []

            prompt_runbook = {

                "title":
                    runbook.get(
                        "title",
                        "Retrieved Runbook"
                    ),

                "category":
                    runbook.get(
                        "category",
                        "Unknown"
                    ),

                "steps":
                    steps

            }

        # --------------------------------------------------
        # Build Prompt
        # --------------------------------------------------

        builder = PromptBuilder(

            current_error=error_text,

            incidents=prompt_incidents,

            runbook=prompt_runbook

        )

        prompt = builder.build()
        
        print("\n" + "=" * 70)
        print("PROMPT SENT TO LLAMA 3")
        print("=" * 70)
        print(prompt)
        print("=" * 70)

        print("\nSending prompt to Llama3...\n")

        analysis = self.client.generate(
            prompt
        )

        print("Analysis completed successfully.")

        return {

            "error": error_text,

            "incidents": incidents,

            "runbook": runbook,

            "analysis": analysis

        }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    analyzer = RCAAnalyzer()

    incidents = [

        {

            "category": "Database",

            "error": "Database timeout",

            "cause": "VPN outage",

            "fix": "Reconnect VPN"

        },

        {

            "category": "Database",

            "error": "Connection refused",

            "cause": "Database server stopped",

            "fix": "Restart database"

        }

    ]

    runbook = {

        "title": "Database Connectivity",

        "category": "Database",

        "content": (
            "Verify VPN connection. "
            "Check database server. "
            "Restart ETL pipeline."
        )

    }

    result = analyzer.analyze(

        "Unable to connect to database",

        incidents,

        runbook

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