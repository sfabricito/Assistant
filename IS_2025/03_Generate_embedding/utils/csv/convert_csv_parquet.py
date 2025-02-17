import pandas as pd

def convert_csv_parquet(input_file, output_file,):
    df = pd.read_csv(input_file)
    
    df.to_parquet(output_file, engine='fastparquet')