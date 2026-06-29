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

from agent.graph import graph
from reports.pdf_report import PDFReport

st.set_page_config(
    page_title="Agentic RAG ETL Dashboard",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Agentic RAG")
st.sidebar.write("Automatic ETL Failure Investigation")
run_button = st.sidebar.button(
    "Run Investigation",
    type="primary",
    use_container_width=True
)
st.sidebar.info("Reads latest ETL log using LangGraph.")

st.title("Agentic RAG System for ETL Failure Analysis")
st.caption("LangGraph + ChromaDB + Llama 3")
st.divider()

if not run_button:
    st.info("Click **Run Investigation**.")
    st.stop()

with st.spinner("Running LangGraph Investigation..."):
    state = {
        "error": "",
        "incidents": [],
        "runbook": {},
        "history": [],
        "analysis": "",
        "confidence": "",
        "pdf_path": ""
    }
    result = graph.invoke(state)

st.success("Investigation Completed")

st.header("Current ETL Error")
st.code(result["error"])

st.divider()

st.header("Historical Incidents")
if result["incidents"]:
    for i, incident in enumerate(result["incidents"], start=1):
        with st.expander(f"Incident {i}"):
            st.write(f"**Category:** {incident.get('category','Unknown')}")
            st.write(f"**Error:** {incident.get('error','Unknown')}")
            st.write(f"**Root Cause:** {incident.get('cause','Unknown')}")
            st.write(f"**Fix:** {incident.get('fix','Unknown')}")
else:
    st.warning("No historical incidents found.")

st.divider()

st.header("Retrieved Runbook")
runbook = result["runbook"]
if runbook:
    st.write(f"**Title:** {runbook.get('title','Unknown')}")
    st.write(f"**Category:** {runbook.get('category','Unknown')}")
    st.markdown(runbook.get("content", "No content available."))
else:
    st.warning("No runbook retrieved.")

st.divider()

st.header("Root Cause Analysis")
st.text_area(
    "Llama 3 Analysis",
    value=result["analysis"],
    height=350,
    disabled=True
)

st.divider()

st.header("PDF Report")

pdf = PDFReport()
try:
    output_file = pdf.generate_report(
        current_error=result["error"],
        incidents=result["incidents"],
        runbook=result["runbook"],
        analysis=result["analysis"]
    )

    result["pdf_path"] = output_file

    with open(output_file, "rb") as f:
        st.download_button(
            "Download PDF Report",
            data=f,
            file_name="ETL_FAILURE_REPORT.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    st.success("PDF generated successfully.")
except Exception as e:
    st.error(f"PDF generation failed: {e}")

st.divider()

st.header("Investigation Summary")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Incidents", len(result["incidents"]))
with c2:
    st.metric("Confidence", result["confidence"])
with c3:
    st.metric("History Records", len(result["history"]))

st.caption(
    "Agentic RAG ETL Failure Analysis | LangGraph • ChromaDB • Ollama • Llama 3 • Streamlit"
)
