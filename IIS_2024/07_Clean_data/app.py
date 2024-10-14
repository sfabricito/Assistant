from utils.clean_csv import clean_csv
from utils.convert_csv_parquet import convert_csv_parquet
from utils.read_file import read_file


if __name__=="__main__":
    clean_csv('./data/globalterrorismdb.csv','./data/globalTerrorism.csv', 32000)
    convert_csv_parquet('./data/globalTerrorism.csv', './data/globalTerrorism20000.parquet')
    read_file('./data/globalTerrorism20000.parquet')