import numpy as np
from .read_file import read_file
from .generate_embeddings import generate_embeddings
from .system.logger import logger

log = logger()

def store_embeddings(file):
    df = read_file(file)
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
    
    for index, row in df.iterrows():
        log.info(f'Row {index+1} read')
        
        for col in ['date', 'location', 'attack_type', 'target_type', 'corporation', 
                    'target', 'orchestrating_group', 'weapon', 'notes', 
                    'scite1', 'scite2', 'scite3']:
            embedding = generate_embeddings(row[col])
            df.at[index, f'{col}_vector'] = np.array2string(
                np.array(embedding), 
                separator=', ',
                formatter={'float_kind': lambda x: f"{x:.18f}"}
            )

    df.to_parquet('./data/globalTerrorismWithEmbeddings.parquet')
    log.info('File with embeddings saved')
