import pyarrow.parquet as pq

def read_file(file):
    parquet_file = pq.ParquetFile(file)
    
    table = parquet_file.read_row_groups([0])
    
    df = table.to_pandas()

    for index, row in df.iterrows():
        # Iterate over each element in the row
        for col, value in row.items():
            print(f"  Column: {col}, Value: {value}")
    
    return df
