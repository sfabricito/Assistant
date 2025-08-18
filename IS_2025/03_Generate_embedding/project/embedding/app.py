import os
import time
import curses
import numpy as np
import pyarrow.parquet as pq
import torch

from dotenv import load_dotenv
from utils.logger import logger
from utils.tools.models import loadModels
from sentence_transformers import SentenceTransformer

# Improve CUDA memory behavior to reduce fragmentation before torch initializes
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')
# Prevent excessive tokenizer threads
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')

load_dotenv()
log = logger()

model = None
models = loadModels()
EMBEDDING_DIRECTORY = os.getenv('EMBEDDING_DIRECTORY')
CLEAN_DATA_DIRECTORY = os.getenv('CLEAN_DATA_DIRECTORY')
BATCH_SIZE = int(os.getenv('EMBEDDING_BATCH_SIZE', '16'))
PREFERRED_DEVICE = os.getenv('EMBEDDING_DEVICE', 'auto')  # 'auto' | 'cuda' | 'cpu'
MAX_SEQ_LENGTH = int(os.getenv('EMBEDDING_MAX_SEQ_LENGTH', '0'))  # 0 = model default


def _select_device(model_name: str) -> str:
    """
    Choose an execution device based on availability and model size.
    - Force CPU for very large models to avoid GPU OOM unless explicitly requested.
    """
    huge_models = {
        'Qwen3-Embedding-8B',
        'E5-mistral-7b-instruct',
    }

    if PREFERRED_DEVICE.lower() == 'cpu':
        return 'cpu'
    if PREFERRED_DEVICE.lower() == 'cuda':
        return 'cuda' if torch.cuda.is_available() else 'cpu'

    # auto
    if model_name in huge_models:
        return 'cpu'
    return 'cuda' if torch.cuda.is_available() else 'cpu'


def _load_model_safely(model_id: str, device: str):
    """
    Try loading the model with mixed precision on CUDA; on failure, fall back to CPU.
    """
    # Prefer float16 on CUDA to reduce memory; CPU stays float32
    model_kwargs = {}
    if device == 'cuda':
        model_kwargs['torch_dtype'] = torch.float16

    try:
        m = SentenceTransformer(model_id, device=device, trust_remote_code=True, model_kwargs=model_kwargs)
        return m, device
    except RuntimeError as e:
        # Typical CUDA OOM -> fallback to CPU
        if 'CUDA out of memory' in str(e) or 'CUDA error' in str(e):
            log.warning(f'CUDA issue while loading {model_id} on GPU; falling back to CPU. {e}')
            try:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                m = SentenceTransformer(model_id, device='cpu')
                return m, 'cpu'
            except Exception as e2:
                raise e2
        raise e

def generate_embeddings(model_name, file, stdscr=None):
    log.info('Generating embeddings with', model_name, file)
    global model

    if model_name in models:
        if stdscr:
            stdscr.addstr(1, 0, f"Generating Embeddings for {model_name}...")
        device = _select_device(model_name)
        model, actual_device = _load_model_safely(models[model_name]['id'], device)
        # Optionally cap max sequence length to save memory with long inputs
        if MAX_SEQ_LENGTH > 0:
            try:
                model.max_seq_length = MAX_SEQ_LENGTH
                log.info(f'Set model.max_seq_length = {MAX_SEQ_LENGTH}')
            except Exception as e:
                log.warning(f'Could not set max_seq_length: {e}')
        log.info(f'Model loaded on device: {actual_device}')
        store_embeddings(model_name, file, stdscr)

def store_embeddings(model_name, file, stdscr=None):
    start_time = time.time()
    df = read_file(f'{CLEAN_DATA_DIRECTORY}/{file}')
    log.info(f'File read: {file}')
    
    vector_columns = ['text']
    
    for col in vector_columns:
        df[f'{col}_vector'] = None

    total_rows = len(df)
    texts = {col: df[col].astype(str).replace({'': 'Null'}) for col in vector_columns}

    # Process in small batches to limit GPU memory usage
    for start in range(0, total_rows, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total_rows)
        if stdscr:
            progress = round(end / total_rows * 100, 1)
            stdscr.addstr(1, 0, f"Generating Embeddings for {file} with {model_name}...")
            stdscr.addstr(2, 0, f"Processing rows {start + 1} - {end} of {total_rows}")
            stdscr.addstr(3, 0, f"Progress... {progress}%")
            stdscr.refresh()
            stdscr.clear()

        for col in vector_columns:
            batch_texts = texts[col].iloc[start:end].tolist()
            batch_embeddings = generateEmbedding(batch_texts)
            for idx, emb in enumerate(batch_embeddings):
                df.at[start + idx, f'{col}_vector'] = np.array(emb, dtype=np.float32).tolist()

        # Release cached GPU memory between batches
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    file_name, file_ext = os.path.splitext(file)
    new_file_name = f'{EMBEDDING_DIRECTORY}/{file_name}_{model_name}{file_ext}'

    df.to_parquet(new_file_name, engine='pyarrow')

    file_size = os.path.getsize(new_file_name) / (1024 * 1024)
    log.info(f'File with embeddings saved: {new_file_name} with size {file_size:.2f} MB')
    end_time = time.time()
    elapsed_time = end_time - start_time
    log.info(f'Total processing time for embedding generation: {elapsed_time:.2f} seconds')

    if stdscr:
        stdscr.addstr(0, 0, "Process Complete!")
        stdscr.refresh()
        curses.napms(1000)

def read_file(file):
    parquet_file = pq.ParquetFile(file)
    table = parquet_file.read_row_groups([0])
    df = table.to_pandas()
    return df

def generateEmbedding(text):
    try:
        # Support both single string and list of strings for batched encode
        if isinstance(text, list):
            if len(text) == 0:
                return []
            embeddings = model.encode(
                text,
                batch_size=BATCH_SIZE,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=False,
            )
            return embeddings.tolist()
        else:
            if isinstance(text, str) and text != '':
                embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=False).tolist()
            else:
                embedding = model.encode('Null', convert_to_numpy=True, normalize_embeddings=False).tolist()
            return embedding
    except Exception as e:
        log.error(f'An error has occur while generating an embedding. {e}')
        try:
            dim = getattr(model, 'get_sentence_embedding_dimension', lambda: 768)()
        except Exception:
            dim = 768
        if isinstance(text, list):
            return [[0.0] * dim for _ in text]
        return [0.0] * dim  # fallback to prevent crash
