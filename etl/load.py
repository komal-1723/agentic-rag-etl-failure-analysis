def load_data(df):

    try:

        print(
            "Data Loaded Successfully"
        )

    except Exception:

        raise ConnectionError(
            "Load Failed"
        )