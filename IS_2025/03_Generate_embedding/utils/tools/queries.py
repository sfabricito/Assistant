import json
from pathlib import Path

def load_queries(json_path: str):
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            queries = json.load(file)
        return queries
    except FileNotFoundError:
        print(f"El archivo no fue encontrado: {json_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON: {e}")
        return []