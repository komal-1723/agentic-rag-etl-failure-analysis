import re


def parse_logs(log_file):
    """
    Returns all ETL errors found in the log.
    """

    errors = []

    with open(log_file, "r") as file:

        for line in file:

            if "ERROR" in line:

                match = re.search(
                    r"ERROR\s*-\s*(.*)",
                    line
                )

                if match:

                    errors.append(
                        match.group(1).strip()
                    )

    return errors


def parse_latest_error(log_file):
    """
    Returns the latest ETL error.
    """

    errors = parse_logs(log_file)

    if not errors:
        return None

    return errors[-1]


if __name__ == "__main__":

    latest = parse_latest_error(
        "logs/etl.log"
    )

    print(latest)