import zipfile
import requests
from .reduce_csv import reduce_csv

def download_data(url):
    response = requests.get(url, verify=True)
    with open('vector_database_wikipedia_articles_embedded.zip', 'wb') as file:
        file.write(response.content)

    with zipfile.ZipFile("vector_database_wikipedia_articles_embedded.zip","r") as zip_ref:
        zip_ref.extractall("../data")

    reduce_csv(
        './data/vector_database_wikipedia_articles_embedded.csv', 
        './data/small_vector_database_wikipedia_articles_embedded.csv', 
        2000
        )
