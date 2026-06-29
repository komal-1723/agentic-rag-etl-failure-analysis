"""
test_llm.py

Runs the complete ETL Failure Analysis pipeline.

Flow

ETL Log
    ↓
Parser
    ↓
Latest Error
    ↓
Retriever
    ↓
Prompt Builder
    ↓
Llama3
    ↓
Root Cause Analysis

"""

from parser.log_parser import parse_latest_error
from llm.analyser import RCAAnalyzer


def main():

    print("=" * 70)
    print("ETL FAILURE ROOT CAUSE ANALYSIS")
    print("=" * 70)

    error = parse_latest_error(
        "logs/etl.log"
    )

    if error is None:

        print("\nNo ETL errors found.")
        return

    print(f"\nLatest Error:\n{error}")

    analyzer = RCAAnalyzer()

    print("\nRunning Investigation...\n")

    report = analyzer.analyze(error)

    print("=" * 70)
    print("ROOT CAUSE ANALYSIS")
    print("=" * 70)

    print(report)

    print("=" * 70)
    print("END OF REPORT")
    print("=" * 70)


if __name__ == "__main__":
    main()