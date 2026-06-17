def transform_data(df):

    # Business Transformation

    df["name"] = df["name"].fillna("UNKNOWN")

    df["name"] = df["name"].str.upper()

    return df


def validate_data(df):

    errors = []

    required_columns = [
        "customer_id",
        "name",
        "email",
        "city",
        "phone"
    ]

    # Schema Validation

    for col in required_columns:

        if col not in df.columns:

            errors.append(
                f"Schema Mismatch: {col}"
            )

    # Stop further checks if schema is wrong

    if errors:
        return errors

    # Missing Email

    if df["email"].isnull().any():

        errors.append(
            "Missing Email Found"
        )

    # Missing City

    if df["city"].isnull().any():

        errors.append(
            "Missing City Found"
        )

    # Missing Name

    if df["name"].isnull().any():

        errors.append(
            "Null Customer Name"
        )

    # Missing Phone

    if df["phone"].isnull().any():

        errors.append(
            "Missing Phone Number"
        )

    # Invalid Phone

    valid_phone_rows = df[
        df["phone"].notnull()
    ]

    invalid_phone = valid_phone_rows[
        valid_phone_rows["phone"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.len() != 10
    ]

    if not invalid_phone.empty:

        errors.append(
            "Invalid Phone Number"
        )

    # Duplicate Customer ID

    duplicate_ids = df[
        df["customer_id"].duplicated()
    ]

    if not duplicate_ids.empty:

        errors.append(
            "Duplicate Customer ID"
        )

    return errors