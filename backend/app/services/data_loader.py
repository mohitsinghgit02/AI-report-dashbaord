import pandas as pd
from app.config import DATA_FOLDER


def load_csv(file_name):

    path = f"{DATA_FOLDER}/{file_name}"

    df = pd.read_csv(path)

    return df
