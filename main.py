import logging

from etl.extract import extract_data

from etl.transform import (
    transform_data,
    validate_data
)

from etl.load import load_data

from classifier.classify import classify_error

from db.database import (
    create_table,
    save_incident
)


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    create_table()

    try:

        logging.info(
            "Extract Started"
        )

        df = extract_data(
            "data/customers.csv"
        )

        logging.info(
            "Transform Started"
        )

        df = transform_data(df)

        logging.info(
            "Validation Started"
        )

        errors = validate_data(df)

        if errors:

            print(
                "\nPipeline Failed\n"
            )

            print(
                "Errors Found:\n"
            )

            for error in errors:

                logging.error(error)

                category = classify_error(
                    error
                )

                save_incident(
                    error,
                    category
                )

                print(
                    f"Error: {error}"
                )

                print(
                    f"Category: {category}\n"
                )

            print(
                "All incidents saved to SQLite"
            )

            return

        logging.info(
            "Load Started"
        )

        load_data(df)

        print(
            "\nPipeline Success\n"
        )

    except FileNotFoundError as e:

        error = str(e)

        logging.error(error)

        category = classify_error(
            error
        )

        save_incident(
            error,
            category
        )

        print(
            "\nPipeline Failed\n"
        )

        print(
            f"Error: {error}"
        )

        print(
            f"Category: {category}"
        )

    except Exception as e:

        error = str(e)

        logging.error(error)

        category = classify_error(
            error
        )

        save_incident(
            error,
            category
        )

        print(
            "\nPipeline Failed\n"
        )

        print(
            f"Error: {error}"
        )

        print(
            f"Category: {category}"
        )


if __name__ == "__main__":

    run_pipeline()