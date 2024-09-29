from utils.clean_csv import clean_csv
from utils.convert_csv_parquet import convert_csv_parquet
from utils.read_file import read_file


if __name__=="__main__":
    clean_csv('./data/globalterrorismdb.csv','./data/globalTerrorism.csv.csv')
    convert_csv_parquet('./data/globalTerrorism.csv.csv', './data/globalTerrorism.csv.parquet')
    read_file('./data/globalTerrorism.csv.parquet')