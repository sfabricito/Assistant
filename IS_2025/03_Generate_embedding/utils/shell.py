import curses
import os
import re

from utils.logger import logger

log = logger()

def csv_shell(stdscr):
    directory = "data/csv"
    curses.curs_set(0)
    
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    except FileNotFoundError:
        files = []

    options = files + ["Back"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"CSV Files in {directory} (Use arrow keys to navigate, ENTER to select)")

        for idx, option in enumerate(options):
            if idx == selected:
                stdscr.addstr(idx + 2, 2, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 2, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("\n"):
            selected_file = options[selected]
            if selected_file == "Back":
                return None, None

            curses.curs_set(1)
            stdscr.clear()
            stdscr.addstr(0, 0, f"Selected: {selected_file}")
            stdscr.addstr(1, 0, "Enter the number of rows to affect: ")

            stdscr.move(1, len("Enter the number of rows to affect: "))

            curses.echo()
            stdscr.refresh()
            rows_input = stdscr.getstr(1, len("Enter the number of rows to affect: "), 10).decode("utf-8").strip()
            curses.noecho()

            if not rows_input.isdigit() or int(rows_input) <= 0:
                return selected_file, 0

            log.info(f"Selected file: {selected_file}, rows: {rows_input}")

            return selected_file, int(rows_input)

def model_shell(stdscr):
    curses.curs_set(0)
    options = [
        "gte-small",
        "gte-base", 
        "gte-large",

        "e5-base-v2",
        "e5-small-v2",
        "e5-large-v2",
        
        "all-mpnet-base-v2", 
        "all-MiniLM-L12-v2", 
        "all-miniLM-L6-v2",
        
        "Back"
        ]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Use arrow keys to navigate. Press ENTER to select.")

        for idx, option in enumerate(options):
            if idx == selected:
                stdscr.addstr(idx + 2, 2, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 2, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("\n"):
            if options[selected] == "Back":
                return None, None
            selected_parquet = parquet_shell(stdscr)
            if selected_parquet is None:
                continue
            return options[selected], selected_parquet

def parquet_shell(stdscr):
    directory = "data/clean"
    curses.curs_set(0)
    
    def natural_sort_key(filename):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', filename)]

    try:
        files = sorted(
            [f for f in os.listdir(directory) if f.endswith(".parquet")],
            key=natural_sort_key
        )
    except FileNotFoundError:
        files = []

    options = files + ["Back"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Parquet Files in {directory} (Use arrow keys to navigate, ENTER to select)")

        for idx, option in enumerate(options):
            if idx == selected:
                stdscr.addstr(idx + 2, 2, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 2, f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("\n"):
            selected_file = options[selected]
            if selected_file == "Back":
                return None
            return selected_file