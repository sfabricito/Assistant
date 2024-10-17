from utils.clean_csv import clean_csv
from utils.convert_csv_parquet import convert_csv_parquet
from utils.read_file import read_file

ROWS = 50

if __name__=="__main__":
    clean_csv('./data/globalterrorismdb.csv','./data/globalTerrorism.csv', ROWS)
    convert_csv_parquet('./data/globalTerrorism.csv', f'./data/globalTerrorism{ROWS}.parquet')
    read_file(f'./data/globalTerrorism{ROWS}.parquet')