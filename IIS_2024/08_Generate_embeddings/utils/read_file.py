import pyarrow.parquet as pq

def read_file(file):
    parquet_file = pq.ParquetFile(file)
    table = parquet_file.read_row_groups([0])
    df = table.to_pandas()
    return df