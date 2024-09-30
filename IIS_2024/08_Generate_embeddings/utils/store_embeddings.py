from .read_file import read_file
from .generate_embeddings import generate_embeddings
from .system.logger import logger

# def store_embeddings():
#     df = read_file('./data/globalTerrorism.csv1000.parquet')
#     log.info('File read')
#     for index, row in df.iterrows():
#         log.info(f'Row {row} read')
#         # Iterate over each element in the row
#         for col, value in row.items():
#             print(f"  Column: {col}, Value: {value}")

from .read_file import read_file
from .generate_embeddings import generate_embeddings
from .system.logger import logger

log = logger()

def store_embeddings():
    df = read_file('./data/globalTerrorism100.parquet')
    log.info('File read')
    
    df['date_vector'] = None
    df['location_vector'] = None
    df['attack_type_vector'] = None
    df['target_type_vector'] = None
    df['corporation_vector'] = None
    df['target_vector'] = None
    df['orchestrating_group_vector'] = None
    df['weapon_vector'] = None
    df['notes_vector'] = None
    df['scite1_vector'] = None
    df['scite2_vector'] = None
    df['scite3_vector'] = None
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        log.info(f'Row {index} read')
        
        embedding = generate_embeddings(row['date'])
        df.at[index, 'date_vector'] = embedding

        embedding = generate_embeddings(row['location'])
        df.at[index, 'location_vector'] = embedding

        embedding = generate_embeddings(row['attack_type'])
        df.at[index, 'attack_type_vector'] = embedding

        embedding = generate_embeddings(row['target_type'])
        df.at[index, 'target_type_vector'] = embedding

        embedding = generate_embeddings(row['corporation'])
        df.at[index, 'corporation_vector'] = embedding

        embedding = generate_embeddings(row['target'])
        df.at[index, 'target_vector'] = embedding

        embedding = generate_embeddings(row['orchestrating_group'])
        df.at[index, 'orchestrating_group_vector'] = embedding

        embedding = generate_embeddings(row['weapon'])
        df.at[index, 'weapon_vector'] = embedding

        embedding = generate_embeddings(row['notes'])
        df.at[index, 'notes_vector'] = embedding

        embedding = generate_embeddings(row['scite1'])
        df.at[index, 'scite1_vector'] = embedding

        embedding = generate_embeddings(row['scite2'])
        df.at[index, 'scite3_vector'] = embedding

        embedding = generate_embeddings(row['scite3'])
        df.at[index, 'scite3_vector'] = embedding

    df.to_parquet('./data/modified_globalTerrorism.parquet')
    log.info('File with embeddings saved')
