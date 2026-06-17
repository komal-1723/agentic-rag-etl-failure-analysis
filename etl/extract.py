import pandas as pd
import os


def extract_data(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "File Not Found"
        )

    df = pd.read_csv(file_path)

    if df.empty:

        raise ValueError(
            "Empty File"
        )

    return df