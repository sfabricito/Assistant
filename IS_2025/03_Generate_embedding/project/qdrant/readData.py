import os
import pandas as pd
from ast import literal_eval
import pyarrow.parquet as pq
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()
log = logger()

VECTOR_COLUMNS = [
    'text_vector'
]

def apply_literal_eval(df, columns):
    for column in columns:
        df[column] = df[column].apply(literal_eval)
    return df

def readData(filename):
    try:
        log.info(f'Reading rows from file {filename}')
        parquet_file_path = f'./data/embedding/{filename}'
        parquet_file = pq.ParquetFile(parquet_file_path)

        table = parquet_file.read()
        article_df = table.to_pandas()

        # NO NECESITAS apply_literal_eval si los vectores ya son listas
        article_df = apply_literal_eval(article_df, VECTOR_COLUMNS)

        article_df['id'] = article_df['id'].astype(str)
        return article_df

    except Exception as e:
        print(e)
        log.error(f'Exception while reading rows. {e}')