import re

def parse_logs(log_file):

    errors = []

    with open(log_file, "r") as file:

        for line in file:

            if "ERROR" in line:

                match = re.search(
                    r"ERROR - (.*)",
                    line
                )

                if match:

                    errors.append(
                        match.group(1)
                    )

    return errors