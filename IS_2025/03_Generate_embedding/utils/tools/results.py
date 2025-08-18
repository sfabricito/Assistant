
import os
import csv
import pandas as pd
from pathlib import Path

def append_to_csv(
    csv_path: str,
    query_id: int,
    modelo_embedding: str,
    distancia: str,
    tipo_query: str,
    mejor_puntaje: float,
    mejor_ataque_id: int,
    query_esperado: bool,
    precision: float
):
    # Asegurarse de que el archivo exista y tenga encabezado
    file_exists = Path(csv_path).is_file()
    
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Query ID", 
            "Modelo de Embedding", 
            "Distancia", 
            "Tipo de Query", 
            "Mejor Puntaje Obtenido", 
            "Mejor Ataque ID", 
            "Query Esperado", 
            "Presicion"
        ],
        delimiter=';')
        
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Query ID": query_id,
            "Modelo de Embedding": modelo_embedding.split("/")[-1],
            "Distancia": distancia,
            "Tipo de Query": f"Tipo {tipo_query}",
            "Mejor Puntaje Obtenido": f"{mejor_puntaje:.8f}".replace('.', ','),
            "Mejor Ataque ID": mejor_ataque_id,
            "Query Esperado": "Sí" if query_esperado else "No",
            "Presicion": precision
        })

def openCSV(ruta_archivo):
    if os.path.exists(ruta_archivo):
        try:
            if ruta_archivo.endswith('.csv'):
                df = pd.read_csv(ruta_archivo, sep=';')
            elif ruta_archivo.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(ruta_archivo)
            else:
                print(f"Formato de archivo no soportado: {ruta_archivo}")
                return None
            return df
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None
    else:
        print(f"El archivo no existe: {ruta_archivo}")
        return None
