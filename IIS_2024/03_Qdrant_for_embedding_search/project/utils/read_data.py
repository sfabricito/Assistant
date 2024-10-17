import os
import pandas as pd
from ast import literal_eval
import pyarrow.parquet as pq
from dotenv import load_dotenv
from .system.logger import logger

load_dotenv()
log = logger()

FILE_NAME = os.getenv('FILE_NAME')
VECTOR_COLUMNS = [
    'date_vector', 'location_vector', 'attack_type_vector',
    'target_type_vector', 'corporation_vector', 'target_vector',
    'orchestrating_group_vector', 'weapon_vector', 'notes_vector',
    'scite1_vector', 'scite2_vector', 'scite3_vector'
]

def apply_literal_eval(df, columns):
    for column in columns:
        df[column] = df[column].apply(literal_eval)
    return df

def read_data():
    try:
        log.info(f'Reading rows from file')
        csv_file_path = f'./data/{FILE_NAME}'
        parquet_file = pq.ParquetFile(csv_file_path)
        
        table = parquet_file.read_row_groups([0])
        article_df = table.to_pandas()

        article_df = apply_literal_eval(article_df, VECTOR_COLUMNS)
        article_df['id'] = article_df['id'].astype(str)

        return article_df
    except Exception as e:
        print(e)
        log.error(f'Exception while reading rows. {e}')
