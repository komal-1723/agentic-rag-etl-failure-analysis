"""
pdf_report.py

Generates professional ETL Failure Reports.

Author: Komal K Project
"""

import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.units import inch


class PDFReport:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Heading1"]
        self.title_style.alignment = TA_CENTER

        self.heading_style = self.styles["Heading2"]

        self.normal_style = self.styles["BodyText"]

    def _add_title(self, story):

        story.append(
            Paragraph(
                "ETL FAILURE ROOT CAUSE ANALYSIS REPORT",
                self.title_style
            )
        )

        story.append(
            Spacer(
                1,
                0.30 * inch
            )
        )

    def _add_metadata(
        self,
        story,
        current_error
    ):

        timestamp = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        story.append(
            Paragraph(
                "<b>Generated On</b>",
                self.heading_style
            )
        )

        story.append(
            Paragraph(
                timestamp,
                self.normal_style
            )
        )

        story.append(
            Spacer(
                1,
                0.15 * inch
            )
        )

        story.append(
            Paragraph(
                "<b>Pipeline Status</b>",
                self.heading_style
            )
        )

        story.append(
            Paragraph(
                "FAILED",
                self.normal_style
            )
        )

        story.append(
            Spacer(
                1,
                0.15 * inch
            )
        )

        story.append(
            Paragraph(
                "<b>Current ETL Error</b>",
                self.heading_style
            )
        )

        story.append(
            Paragraph(
                current_error,
                self.normal_style
            )
        )

        story.append(
            Spacer(
                1,
                0.25 * inch
            )
        )

    def _add_incidents(
        self,
        story,
        incidents
    ):

        story.append(
            Paragraph(
                "Retrieved Historical Incidents",
                self.heading_style
            )
        )

        story.append(
            Spacer(
                1,
                0.10 * inch
            )
        )

        if not incidents:

            story.append(
                Paragraph(
                    "No similar incidents found.",
                    self.normal_style
                )
            )

            story.append(
                Spacer(
                    1,
                    0.20 * inch
                )
            )

            return

        for index, incident in enumerate(
                incidents,
                start=1
        ):

            story.append(
                Paragraph(
                    f"<b>Incident {index}</b>",
                    self.normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Category:</b> {incident.get('category','Unknown')}",
                    self.normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Error:</b> {incident.get('error','Unknown')}",
                    self.normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Root Cause:</b> {incident.get('cause','Unknown')}",
                    self.normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Fix:</b> {incident.get('fix','Unknown')}",
                    self.normal_style
                )
            )

            story.append(
                Spacer(
                    1,
                    0.20 * inch
                )
            )
    def _add_runbook(
        self,
        story,
        runbook
    ):
        """
        Add retrieved runbook section.
        """

        story.append(
            Paragraph(
                "Retrieved Runbook",
                self.heading_style
            )
        )

        story.append(
            Spacer(
                1,
                0.10 * inch
            )
        )

        if not runbook:

            story.append(
                Paragraph(
                    "No runbook found.",
                    self.normal_style
                )
            )

            story.append(
                Spacer(
                    1,
                    0.20 * inch
                )
            )

            return

        story.append(
            Paragraph(
                f"<b>Category:</b> {runbook.get('category', 'Unknown')}",
                self.normal_style
            )
        )

        story.append(
            Spacer(
                1,
                0.10 * inch
            )
        )

        story.append(
            Paragraph(
                "<b>Troubleshooting Guide</b>",
                self.normal_style
            )
        )

        story.append(
            Paragraph(
                runbook.get(
                    "content",
                    "No runbook available."
                ),
                self.normal_style
            )
        )

        story.append(
            Spacer(
                1,
                0.25 * inch
            )
        )

    def _add_llm_analysis(
        self,
        story,
        analysis
    ):
        """
        Add Llama 3 Root Cause Analysis.
        """

        story.append(
            Paragraph(
                "LLM Root Cause Analysis",
                self.heading_style
            )
        )

        story.append(
            Spacer(
                1,
                0.10 * inch
            )
        )

        if not analysis:

            story.append(
                Paragraph(
                    "No analysis generated.",
                    self.normal_style
                )
            )

            story.append(
                Spacer(
                    1,
                    0.20 * inch
                )
            )

            return

        sections = analysis.split("\n")

        for line in sections:

            line = line.strip()

            if not line:
                continue

            if (
                line.startswith("Pipeline Status")
                or line.startswith("Category")
                or line.startswith("Severity")
                or line.startswith("Confidence")
                or line.startswith("Root Cause")
                or line.startswith("Recommendations")
            ):

                story.append(
                    Paragraph(
                        f"<b>{line}</b>",
                        self.normal_style
                    )
                )

            else:

                story.append(
                    Paragraph(
                        line,
                        self.normal_style
                    )
                )

        story.append(
            Spacer(
                1,
                0.30 * inch
            )
        )
    def generate_report(
        self,
        current_error,
        incidents,
        runbook,
        analysis,
        output_path="reports/ETL_FAILURE_REPORT.pdf"
    ):

        output_dir = os.path.dirname(output_path)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        doc = SimpleDocTemplate(output_path)

        story = []

        self._add_title(story)

        self._add_metadata(
            story,
            current_error
        )

        self._add_incidents(
            story,
            incidents
        )

        self._add_runbook(
            story,
            runbook
        )

        self._add_llm_analysis(
            story,
            analysis
        )

        doc.build(story)

        print("\nPDF Report Generated Successfully")
        print(f"Saved at : {output_path}")

        return output_path


if __name__ == "__main__":

    pdf = PDFReport()

    current_error = (
        "Unable to connect to database."
    )

    incidents = [
        {
            "category": "Database",
            "error": "Database timeout",
            "cause": "VPN outage",
            "fix": "Restart VPN Gateway"
        },
        {
            "category": "Database",
            "error": "Connection refused",
            "cause": "Database server stopped",
            "fix": "Start database service"
        }
    ]

    runbook = {
        "category": "Database",
        "content":
        (
            "1. Verify VPN connectivity<br/>"
            "2. Check database server<br/>"
            "3. Verify firewall rules<br/>"
            "4. Restart ETL Pipeline"
        )
    }

    analysis = """
Pipeline Status: FAILED

Category: Database

Severity: HIGH

Confidence: 91%

Root Cause:
The ETL pipeline failed because the database
server could not be reached due to a VPN
connectivity issue.

Recommendations:
1. Verify VPN connectivity.
2. Restart the database service.
3. Retry the ETL pipeline.
"""

    pdf.generate_report(
        current_error=current_error,
        incidents=incidents,
        runbook=runbook,
        analysis=analysis
    )