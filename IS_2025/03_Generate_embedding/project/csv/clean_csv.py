import os
import tempfile
import csv
import time
import random
import curses
from project.csv.convert_csv_parquet import convert_csv_parquet

def open_csv(input_file, output_file, num_rows, stdscr=None):
    with open(input_file, mode='r', newline='', encoding='ISO-8859-1') as infile:
        reader = list(csv.reader(infile))
        header = reader[0]
        data = reader[1:]
        
        selected_rows = random.sample(data, num_rows)

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(
                [
                    "id", 
                    "date", 
                    "location", 
                    "attack_type", 
                    "target_type", 
                    "target", 
                    "orchestrating_group", 
                    "motive",
                    "weapon", 
                    "deceased", 
                    "comments",
                    "text"
                ])
            
            total_rows = len(selected_rows)
            for i, row in enumerate(selected_rows):
                row_to_insert = format_row(row, i)
                if row_to_insert:
                    writer.writerow(row_to_insert)

                if stdscr:
                    progress = int((i + 1) / total_rows * 100)
                    stdscr.addstr(3, 0, f"Rows processed: {i + 1}/{total_rows}")
                    stdscr.addstr(4, 0, f"Processing CSV... {progress}%")
                    stdscr.refresh()
                    time.sleep(0.05)

def join_non_empty(*args):
    return ", ".join(str(arg) for arg in args if arg not in [None, "", " "]).strip()

def clean_text(value):
    return "" if not value or value.strip() == "" or value.strip() == "Unknown" or value == "null" else value

def format_row(row, id):
    result = [
        id,  # id
        row[16],  # date
        join_non_empty(row[1], row[0], row[2], row[3], row[4]),  # location
        row[5],  # attack type
        row[6],  # target type
        row[7],  # target
        row[8],  # orchestrating_group
        clean_text(row[9]),  # motive (removes empty or space-only text)
        join_non_empty(row[10], row[11], row[12]),  # weapon
        row[13],  # deceased
        join_non_empty(row[14], row[15]),  # comments
        row[17],  # text
    ]

    return result


def clean_csv(input_file, rows=10, stdscr=None):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    
    try:
        if stdscr:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Cleaning CSV: {input_file}")
            stdscr.refresh()

        open_csv(f'data/csv/{input_file}', temp_file.name, rows, stdscr)

        output_dir = "./data/clean"
        os.makedirs(output_dir, exist_ok=True)

        output_file = f"{output_dir}/globalTerrorism_{rows}.parquet"

        if stdscr:
            stdscr.addstr(4, 0, "Converting to Parquet...")
            stdscr.refresh()

        convert_csv_parquet(temp_file.name, output_file)

        if stdscr:
            stdscr.addstr(5, 0, "Process Complete!")
            stdscr.refresh()
            curses.napms(1000)

    finally:
        if stdscr:
            curses.curs_set(0)
        os.remove(temp_file.name)