import pandas as pd
from ast import literal_eval

def read_data():
    try:
        csv_file_path = './data/small_vector_database_wikipedia_articles_embedded.csv'
        article_df = pd.read_csv(csv_file_path)
        
        article_df['title_vector'] = article_df['title_vector'].apply(literal_eval)
        article_df['content_vector'] = article_df['content_vector'].apply(literal_eval)
        article_df['vector_id'] = article_df['vector_id'].apply(str)
        
        return article_df
    except Exception as e:
        print(f"Exception: {e}") 