import os
import curses
import json
import qdrant_client 

from typing import Optional
from dotenv import load_dotenv
from utils.logger import logger
from utils.tools.results import append_to_csv
from project.qdrant.query import query_qdrant
from utils.tools.saveListTxt import saveListTxt
from sentence_transformers import SentenceTransformer

load_dotenv()
log = logger()

def askText(stdscr, text = "Enter the text to search (press ENTER twice to search)s:"):
    stdscr.clear()
    stdscr.addstr(0, 0, text)
    curses.echo()
    
    input_lines = []
    y = 1

    while True:
        stdscr.move(y, 0)
        line = stdscr.getstr().decode("utf-8").strip()

        if line == "":
            break  # Exit if user presses ENTER on an empty line

        input_lines.append(line)
        y += 1

    curses.noecho()
    return "\n".join(input_lines)

def searchMenu(stdscr):
    stdscr.clear()
    
    query = askText(stdscr)  # Get the search query from the user
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"Searching for: {query}")
    
    # Call the query function with the provided query
    results = query_qdrant(query)
    saveListTxt(results, "./data/search/search.txt")  # Save results to a file
    
    stdscr.addstr(2, 0, "Search Results:")
    
    for idx, result in enumerate(results):
        stdscr.addstr(idx + 3, 2, f"Result {idx + 1}: {result}")
    
    stdscr.addstr(len(results) + 4, 0, "Press any key to go back...")
    stdscr.getch()  # Wait for user input before returning

def searchParamsMenu(stdscr):
    stdscr.clear()
    
    query = askText(stdscr, "Enter search query:")  # Get the search query from the user

    # Ask for standard parameters first
    stdscr.clear()
    stdscr.addstr(0, 0, "Configure search parameters (press Enter to use default):")

    # Now collect filters (key-value pairs for payload filtering)
    stdscr.clear()
    stdscr.addstr(0, 0, "Add filters for metadata search (leave empty to finish):")
    
    filters = {}
    while True:
        key = askText(stdscr, "Enter a metadata field to filter (or leave empty to finish):")
        if not key:
            break
        value = askText(stdscr, f"Enter the value for '{key}':")
        filters[key] = value

    stdscr.clear()
    stdscr.addstr(0, 0, f"Searching for: {query}")
    if filters:
        stdscr.addstr(2, 0, f"Filters: {filters}")

    # Call the query function with the provided query and parameters
    results = query_qdrant(
        query=query,
        top_k=5,
        filters=filters if filters else None
    )
    
    saveListTxt(results, "./data/search/search.txt")  # Save results to a file
    
    result_start_line = 3 if filters else 2
    stdscr.addstr(result_start_line + 1, 0, "Search Results:")

    for idx, result in enumerate(results):
        display_line = result_start_line + idx + 2
        stdscr.addstr(display_line, 2, f"Result {idx + 1}: {result}")
    
    stdscr.addstr(result_start_line + len(results) + 3, 0, "Press any key to go back...")
    stdscr.getch()  # Wait for user input before returning

def processAllQueries(stdscr):
    json_path = "./data/queries/queries.json"
    csv_output_path = "./data/search/results.csv"

    with open(json_path, 'r', encoding='utf-8') as file:
        queries = json.load(file)

    total_queries = len(queries)
    log.warning(f"Starting processing of {total_queries} queries...")


    QDRANT_HOST = os.getenv('QDRANT_HOST')
    QDRANT_PORT = os.getenv('QDRANT_PORT')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
    qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    model = SentenceTransformer(EMBEDDING_MODEL)
    

    for idx, q in enumerate(queries, start=1):
        query_id = q["id"]
        query_text = q["query"]
        tipo_query = q["query_type"]
        expected_attacks = set(q.get("attacks_related", []))
        filters: Optional[dict] = q.get("filters")  
        
        log.warning(f"Processing query {idx}/{total_queries} - ID: {query_id}, Type: {tipo_query}, Filters: {filters}")

        stdscr.clear()
        stdscr.addstr(0, 0, f"Processing queries... {idx}/{total_queries}")
        stdscr.addstr(1, 0, f"Current Query ID: {query_id}, Type: {tipo_query}")
        if filters:
            stdscr.addstr(2, 0, f"Filters: {filters}")
        stdscr.refresh()

        results = query_qdrant(
            query=query_text,
            top_k=5,
            filters=filters if filters else None,
            qdrant=qdrant,
            model=model,
        )

        log.warning(f"Query ID: {query_id}, Results: {results}")

        if not results:
            log.info(f"No results for query ID {query_id}, skipping.")
            continue

        log.warning(f"Processing results for query ID {query_id}...")
        best_result = results[0]
        mejor_ataque_id = best_result.id
        mejor_puntaje = best_result.score

        query_esperado = mejor_ataque_id in expected_attacks

        retrieved_ids = [res.id for res in results]
        true_positives = len(set(retrieved_ids) & expected_attacks)
        precision = true_positives / 5

        del results


        log.info(f"Best attack ID: {mejor_ataque_id} with score: {mejor_puntaje}")
        log.info(f"Precision calculated: {precision:.4f}")

        append_to_csv(
            csv_path=csv_output_path,
            query_id=query_id,
            modelo_embedding=os.getenv('EMBEDDING_MODEL'),
            distancia=os.getenv('DISTANCE'),
            tipo_query=tipo_query,
            mejor_puntaje=mejor_puntaje,
            mejor_ataque_id=mejor_ataque_id,
            query_esperado=query_esperado,
            precision=precision
        )

    log.info("All queries processed successfully.")
    stdscr.addstr(4, 0, "Processing complete! Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()
