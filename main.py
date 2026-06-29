import logging

from etl.extract import extract_data
from etl.transform import transform_data, validate_data
from etl.load import load_data

from classifier.classify import classify_error
from db.database import (
    create_table,
    save_incident
)

from agent.graph import graph

from reports.pdf_report import PDFReport


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# ETL PIPELINE
# ==========================================================

def run_pipeline():

    create_table()

    try:

        logging.info("Extract Started")

        df = extract_data(
            "data/customers.csv"
        )

        logging.info("Transform Started")

        df = transform_data(df)

        logging.info("Validation Started")

        errors = validate_data(df)

        if errors:

            print("\n========== PIPELINE FAILED ==========\n")

            for error in errors:

                logging.error(error)

                category = classify_error(error)

                save_incident(
                    error,
                    category,
                    "Unknown",
                    "Pending Investigation"
                    
                )

                print(f"Error    : {error}")
                print(f"Category : {category}")
                print("-" * 50)

            print("\nIncidents saved to SQLite.\n")

            return False

        logging.info("Load Started")

        load_data(df)

        logging.info("Pipeline Completed Successfully")

        print("\n========== PIPELINE SUCCESS ==========\n")

        return True

    except Exception as e:

        error = str(e)

        logging.error(error)

        category = classify_error(error)

        save_incident(
            error,
            category,
            "Runtime Exception",
            "Check application logs"
        )

        print("\n========== PIPELINE FAILED ==========\n")
        print(error)

        return False


# ==========================================================
# LANGGRAPH RCA
# ==========================================================

def run_agent():

    print("\n")
    print("=" * 70)
    print("STARTING LANGGRAPH INVESTIGATION")
    print("=" * 70)

    initial_state = {

        "error": "",

        "incidents": [],

        "runbook": {},

        "history": [],

        "analysis": "",

        "confidence": "",

        "pdf_path": ""

    }

    result = graph.invoke(
        initial_state
    )

    return result


# ==========================================================
# PDF
# ==========================================================

def generate_pdf(result):

    pdf = PDFReport()

    output_path = pdf.generate_report(

        current_error=result["error"],

        incidents=result["incidents"],

        runbook=result["runbook"],

        analysis=result["analysis"]

    )

    return output_path


# ==========================================================
# SUMMARY
# ==========================================================

def print_summary(result, pdf_path):

    print("\n")
    print("=" * 70)
    print("INVESTIGATION SUMMARY")
    print("=" * 70)

    print("\nCurrent Error")
    print(result["error"])

    print("\nHistorical Incidents")
    print(len(result["incidents"]))

    if result["runbook"]:

        print("\nRunbook Category")
        print(
            result["runbook"].get(
                "category",
                "Unknown"
            )
        )

    else:

        print("\nRunbook")
        print("Not Found")

    print("\nConfidence")
    print(result["confidence"])

    print("\nLLM Root Cause Analysis\n")

    print(result["analysis"])

    print("\nPDF Report")

    print(pdf_path)

    print("\n")
    print("=" * 70)
    print("SYSTEM COMPLETED SUCCESSFULLY")
    print("=" * 70)


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n")
    print("=" * 70)
    print("AGENTIC RAG ETL FAILURE ANALYSIS SYSTEM")
    print("=" * 70)

    print("\nRunning ETL Pipeline...\n")

    success = run_pipeline()

    if success:

        print("\nNo investigation required.")

        return

    result = run_agent()

    pdf_path = generate_pdf(
        result
    )
    result["pdf_path"] = pdf_path

    print_summary(
        result,
        pdf_path
    )
   


# ==========================================================
# ENTRY
# ==========================================================

if __name__ == "__main__":

    main()