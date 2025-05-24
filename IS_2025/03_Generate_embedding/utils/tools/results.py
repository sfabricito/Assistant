import csv
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
        ])
        
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Query ID": query_id,
            "Modelo de Embedding": modelo_embedding,
            "Distancia": distancia,
            "Tipo de Query": tipo_query,
            "Mejor Puntaje Obtenido": mejor_puntaje,
            "Mejor Ataque ID": mejor_ataque_id,
            "Query Esperado": "Sí" if query_esperado else "No",
            "Presicion": precision
        })