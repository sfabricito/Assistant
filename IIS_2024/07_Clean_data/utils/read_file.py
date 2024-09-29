import pandas as pd

def read_file(file):
    df = pd.read_parquet(file)
    print(df)
