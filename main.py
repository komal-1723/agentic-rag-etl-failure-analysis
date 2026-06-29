import logging

from etl.extract import extract_data
from etl.transform import transform_data, validate_data
from etl.load import load_data

from classifier.classify import classify_error
from db.database import create_table, save_incident

from parser.log_parser import parse_latest_error
from llm.analyser import RCAAnalyzer
from reports.pdf_report import PDFReport


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    create_table()

    try:

        logging.info("Extract Started")

        df = extract_data("data/customers.csv")

        logging.info("Transform Started")

        df = transform_data(df)

        logging.info("Validation Started")

        errors = validate_data(df)

        if errors:

            print("\nPipeline Failed\n")
            print("Errors Found:\n")

            for error in errors:

                logging.error(error)

                category = classify_error(error)

                save_incident(error, category)

                print(f"Error: {error}")
                print(f"Category: {category}\n")

            print("All incidents saved to SQLite")

            return False

        logging.info("Load Started")

        load_data(df)

        print("\nPipeline Success\n")

        return True

    except FileNotFoundError as e:

        error = str(e)

        logging.error(error)

        category = classify_error(error)

        save_incident(error, category)

        print("\nPipeline Failed\n")
        print(f"Error: {error}")
        print(f"Category: {category}")

        return False

    except Exception as e:

        error = str(e)

        logging.error(error)

        category = classify_error(error)

        save_incident(error, category)

        print("\nPipeline Failed\n")
        print(f"Error: {error}")
        print(f"Category: {category}")

        return False


def run_investigation():

    print("\n" + "=" * 70)
    print("STARTING ETL FAILURE INVESTIGATION")
    print("=" * 70)

    latest_error = parse_latest_error("logs/pipeline.log")

    if latest_error is None:

        print("No ETL errors found.")
        return None

    print(f"\nLatest Error:\n{latest_error}")

    analyzer = RCAAnalyzer()

    result = analyzer.analyze(latest_error)

    pdf = PDFReport()

    output_path = pdf.generate_report(
        current_error=result["error"],
        incidents=result["incidents"],
        runbook=result["runbook"],
        analysis=result["analysis"]
    )

    print(f"\nPDF Generated: {output_path}")

    return result


def main():

    print("=" * 70)
    print("AGENTIC RAG ETL FAILURE ANALYSIS SYSTEM")
    print("=" * 70)

    print("\nRunning ETL Pipeline...\n")

    pipeline_success = run_pipeline()

    if pipeline_success:

        print("\nPipeline completed successfully.")
        print("No investigation required.")
        return

    print("\nRunning Investigation...\n")

    result = run_investigation()

    if result is None:

        print("\nNo investigation required.")
        return

    print("\n" + "=" * 70)
    print("INVESTIGATION SUMMARY")
    print("=" * 70)

    print(f"\nCurrent Error:\n{result['error']}")
    print(f"\nHistorical Incidents Retrieved: {len(result['incidents'])}")

    if result["runbook"]:

        print(
            f"Runbook Category: "
            f"{result['runbook'].get('category', 'Unknown')}"
        )

    else:

        print("Runbook: Not Found")

    print("\nLLM Analysis\n")
    print(result["analysis"])

    print("\n" + "=" * 70)
    print("SYSTEM COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()