"""
prompt_builder.py

Builds a structured prompt for Llama 3 using:

1. Current ETL Error
2. Similar Historical Incidents
3. Retrieved Runbook

Author: Komal K Project
"""

from typing import List, Dict


class PromptBuilder:
    """
    Builds prompts for ETL Root Cause Analysis.
    """

    SYSTEM_PROMPT = """
You are a Senior Data Engineer.

You analyze ETL pipeline failures.

You are provided with:

1. Current ETL Error
2. Similar Historical Incidents
3. Retrieved Troubleshooting Runbook

Use ONLY the supplied information.

Return ONLY the following format.

Pipeline Status:
Category:
Severity:
Confidence:

Root Cause:
<root cause>

Recommendations:
1.
2.
3.

Do not invent information.
Use the retrieved incidents and runbook whenever possible.
"""

    def __init__(
        self,
        current_error: str,
        incidents: List[Dict],
        runbook: Dict
    ):

        self.current_error = current_error
        self.incidents = incidents
        self.runbook = runbook

    # ---------------------------------------------------------
    # Historical Incidents
    # ---------------------------------------------------------

    def _format_incidents(self):

        if not self.incidents:

            return "No similar incidents found."

        text = ""

        for index, incident in enumerate(
            self.incidents,
            start=1
        ):

            text += (
                f"\nIncident {index}\n"
                f"Category : {incident.get('category','Unknown')}\n"
                f"Error : {incident.get('error','')}\n"
                f"Root Cause : {incident.get('root_cause','')}\n"
                f"Solution : {incident.get('solution','')}\n"
            )

        return text

    # ---------------------------------------------------------
    # Runbook
    # ---------------------------------------------------------

    def _format_runbook(self):

        if not self.runbook:

            return "No runbook available."

        title = self.runbook.get(
            "title",
            "Retrieved Runbook"
        )

        category = self.runbook.get(
            "category",
            "Unknown"
        )

        content = self.runbook.get(
            "content",
            "No runbook available."
        )

        text = (
            f"Runbook Title : {title}\n"
            f"Category : {category}\n\n"
            f"Troubleshooting Guide:\n"
            f"{content}"
        )

        return text

    # ---------------------------------------------------------
    # Build Prompt
    # ---------------------------------------------------------

    def build(self):

        prompt = f"""
{self.SYSTEM_PROMPT}

==================================================
CURRENT ETL FAILURE
==================================================

{self.current_error}

==================================================
SIMILAR HISTORICAL INCIDENTS
==================================================

{self._format_incidents()}

==================================================
RETRIEVED RUNBOOK
==================================================

{self._format_runbook()}

==================================================
TASK
==================================================

Analyze the ETL failure.

Return ONLY:

Pipeline Status:
Category:
Severity:
Confidence:

Root Cause:

Recommendations:

"""

        return prompt.strip()


# ---------------------------------------------------------
# Example Test
# ---------------------------------------------------------

if __name__ == "__main__":

    current_error = (
        "Unable to connect to database."
    )

    incidents = [

        {
            "category": "Database",
            "error": "Database timeout",
            "root_cause": "VPN outage",
            "solution": "Reconnect VPN"
        },

        {
            "category": "Database",
            "error": "Connection refused",
            "root_cause": "Database server stopped",
            "solution": "Restart database"
        }

    ]

    runbook = {

        "title": "Database Connectivity",

        "category": "Database",

        "content":
        (
            "1. Verify VPN connection\n"
            "2. Check database server\n"
            "3. Restart ETL pipeline"
        )

    }

    builder = PromptBuilder(

        current_error=current_error,

        incidents=incidents,

        runbook=runbook

    )

    print(builder.build())