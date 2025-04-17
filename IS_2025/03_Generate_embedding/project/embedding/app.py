import os
import time
import curses
import numpy as np
import pyarrow.parquet as pq

from utils.logger import logger
from sentence_transformers import SentenceTransformer
from utils.tools.models import loadModels


log = logger()

model = None

models = loadModels()


def generate_embeddings(model_name, file, stdscr=None):
    log.info('Generate embedding', model_name, file)
    global model

    if model_name in models:
        stdscr.addstr(1, 0, f"Generating Embeddings for {model_name}...")
        model = SentenceTransformer(models[model_name]['id'])
        store_embeddings(model_name, file, stdscr)

def store_embeddings(model_name, file, stdscr=None):
    start_time = time.time()
    df = read_file(f'./data/clean/{file}')
    log.info(f'File read: {file}')
    
    vector_columns = [
        'text'
    ]
    
    for col in vector_columns:
        df[f'{col}_vector'] = None
    

    for index, row in df.iterrows():
        total_rows = len(df)
        progress = round((index + 1) / total_rows * 100, 1)
        stdscr.addstr(1, 0, f"Generating Embeddings for {file} with {model_name}...")
        stdscr.addstr(2, 0, f"Processing row {index + 1}")
        stdscr.addstr(3, 0, f"Progress... {progress}%")
        stdscr.refresh()
        stdscr.clear()

        log.info(f'Row {index+1} read')

        for col in vector_columns:
            embedding = generate_embedding(row[col])
            df.at[index, f'{col}_vector'] = np.array2string(
                np.array(embedding), 
                separator=', ',
                formatter={'float_kind': lambda x: f"{x:.18f}"}
            )

    file_name, file_ext = os.path.splitext(file)
    new_file_name = f'./data/embedding/{file_name}_{model_name}{file_ext}'


    df.to_parquet(new_file_name)
    
    file_size = os.path.getsize(new_file_name) / (1024 * 1024)
    log.info(f'File with embeddings saved: {new_file_name}')
    log.info(f'File size: {file_size:.2f} MB')
    end_time = time.time()
    elapsed_time = end_time - start_time
    log.info(f'Total processing time: {elapsed_time:.2f} seconds')

    
    if stdscr:
        stdscr.addstr(0, 0, "Process Complete!")
        stdscr.refresh()
        curses.napms(1000)

def read_file(file):
    parquet_file = pq.ParquetFile(file)
    table = parquet_file.read_row_groups([0])
    df = table.to_pandas()
    return df

def generate_embedding(text):
    try:
        if isinstance(text, str) and text != '':
            embedding = model.encode(text).tolist()
        else:
            embedding = model.encode('Null').tolist()
        return embedding
    except Exception as e:
        log.error(f'An error has occur while generating an embedding. {e}')