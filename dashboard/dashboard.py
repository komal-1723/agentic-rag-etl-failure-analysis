"""
dashboard.py

Agentic RAG ETL Failure Analysis Dashboard

Run:

streamlit run dashboard/dashboard.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st

from parser.log_parser import (
    parse_latest_error
)

from llm.analyser import (
    RCAAnalyzer
)

from reports.pdf_report import (
    PDFReport
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Agentic RAG ETL Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("Agentic RAG")

st.sidebar.markdown("---")

st.sidebar.write(
    "Automatic ETL Failure Investigation"
)

run_button = st.sidebar.button(
    "Run Investigation",
    type="primary",
    use_container_width=True
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Reads latest ETL log automatically."
)

# ----------------------------------------------------
# Main Title
# ----------------------------------------------------

st.title(
    "Agentic RAG System for ETL Failure Analysis"
)

st.caption(
    "Automatic Root Cause Analysis using RAG + Llama 3"
)

st.markdown("---")

# ----------------------------------------------------
# Wait until user clicks
# ----------------------------------------------------

if not run_button:

    st.info(
        "Click **Run Investigation** from the sidebar."
    )

    st.stop()

# ----------------------------------------------------
# Read Latest Error
# ----------------------------------------------------

error = parse_latest_error(
    "logs/pipeline.log"
)

if error is None:

    st.error(
        "No ETL errors found in pipeline.log"
    )

    st.stop()

# ----------------------------------------------------
# Run Analyzer
# ----------------------------------------------------

analyzer = RCAAnalyzer()

with st.spinner(
    "Investigating ETL Failure..."
):

    result = analyzer.analyze(
        error
    )

st.success(
    "Investigation Completed"
)

# ----------------------------------------------------
# Current Error
# ----------------------------------------------------

st.header(
    "Current ETL Error"
)

st.code(
    result["error"]
)

st.markdown("---")

# ----------------------------------------------------
# Historical Incidents
# ----------------------------------------------------

st.header(
    "Similar Historical Incidents"
)

incidents = result["incidents"]

if incidents:

    for index, incident in enumerate(
        incidents,
        start=1
    ):

        with st.expander(
            f"Incident {index}"
        ):

            st.write(
                f"**Category:** {incident.get('category','Unknown')}"
            )

            st.write(
                f"**Error:** {incident.get('error','Unknown')}"
            )

            st.write(
                f"**Root Cause:** {incident.get('cause','Unknown')}"
            )

            st.write(
                f"**Fix:** {incident.get('fix','Unknown')}"
            )

else:

    st.warning(
        "No similar incidents found."
    )

st.markdown("---")

# ----------------------------------------------------
# Runbook
# ----------------------------------------------------

st.header(
    "Retrieved Runbook"
)

runbook = result["runbook"]

if runbook:

    st.write(
        f"**Title:** {runbook.get('title','Unknown')}"
    )

    st.write(
        f"**Category:** {runbook.get('category','Unknown')}"
    )

    st.markdown(
        runbook.get(
            "content",
            "No runbook available."
        )
    )

else:

    st.warning(
        "No runbook found."
    )

st.markdown("---")
# ----------------------------------------------------
# LLM Analysis
# ----------------------------------------------------

st.header(
    "Root Cause Analysis"
)

st.text_area(
    label="Llama 3 Output",
    value=result["analysis"],
    height=350,
    disabled=True
)

st.markdown("---")

# ----------------------------------------------------
# PDF Report
# ----------------------------------------------------

st.header(
    "PDF Report"
)

pdf = PDFReport()

try:

    output_file = pdf.generate_report(
        current_error=result["error"],
        incidents=result["incidents"],
        runbook=result["runbook"],
        analysis=result["analysis"]
    )

    st.success(
        "PDF Report Generated Successfully"
    )

    with open(
        output_file,
        "rb"
    ) as pdf_file:

        st.download_button(

            label="Download PDF Report",

            data=pdf_file,

            file_name="ETL_FAILURE_REPORT.pdf",

            mime="application/pdf",

            use_container_width=True

        )

except Exception as e:

    st.error(
        f"Unable to generate PDF.\n\n{e}"
    )

st.markdown("---")

# ----------------------------------------------------
# Investigation Summary
# ----------------------------------------------------

st.header(
    "Investigation Summary"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Incidents Retrieved",
        len(result["incidents"])
    )

with col2:

    if result["runbook"]:

        st.metric(
            "Runbook Retrieved",
            "Yes"
        )

    else:

        st.metric(
            "Runbook Retrieved",
            "No"
        )

st.markdown("---")

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.caption(
    "Agentic RAG System for ETL Failure Analysis | "
    "Powered by ChromaDB • Sentence Transformers • Ollama • Llama 3 • Streamlit"
)