def classify_error(error):

    error = error.lower()

    if "database" in error:
        return "Database"

    if "load failed" in error:
        return "Database"

    if "schema" in error:
        return "Schema"

    if "file" in error:
        return "File"

    if "empty file" in error:
        return "File"

    if (
        "missing" in error
        or "invalid" in error
        or "duplicate" in error
        or "null" in error
    ):
        return "Data Quality"

    return "Unknown"