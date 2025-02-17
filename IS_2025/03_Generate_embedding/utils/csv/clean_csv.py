import os
import tempfile
import csv
import time
import random
import curses
from utils.csv.convert_csv_parquet import convert_csv_parquet

def open_csv(input_file, output_file, num_rows, stdscr=None):
    with open(input_file, mode='r', newline='', encoding='ISO-8859-1') as infile:
        reader = list(csv.reader(infile))
        header = reader[0]
        data = reader[1:]
        
        selected_rows = random.sample(data, num_rows)

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["id", "date", "location", "attack_type", "target_type", "corporation", "target", "orchestrating_group", "weapon", "deceased", "notes", "scite1", "scite2", "scite3"])
            
            total_rows = len(selected_rows)
            for i, row in enumerate(selected_rows):
                row_to_insert = format_row(row)
                if row_to_insert:
                    writer.writerow(row_to_insert)

                if stdscr:
                    progress = int((i + 1) / total_rows * 100)
                    stdscr.addstr(3, 0, f"Processing CSV... {progress}%")
                    stdscr.refresh()
                    time.sleep(0.05)


def format_row(row):
    result = [
        row[0],  # id
        f"{row[1]}-{row[2]}-{row[3]}",  # date
        f"{row[8]}, {row[11]}, {row[12]}",  # location
        row[29],  # attack type
        f"{row[35]}, {row[37]}",  # type_target
        row[38],  # corporation
        row[39],  # target
        row[58],  # orchestrating_group
    ]

    weapon = "unknown"
    if row[82] or row[84]:
        weapon = f"{row[82]}, {row[84]}" if row[82] and row[84] else row[82] or row[84]
    result.append(weapon)

    result.append(row[98] if row[98] else 'unknown')

    additional_info = [row[idx] if row[idx] else 'unknown' for idx in [125, 126, 127, 128]]
    if all(info == 'unknown' for info in additional_info):
        return []
    
    result.extend(additional_info)

    return result

def clean_csv(input_file, rows=100, stdscr=None):
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
        curses.curs_set(0)
        os.remove(temp_file.name)