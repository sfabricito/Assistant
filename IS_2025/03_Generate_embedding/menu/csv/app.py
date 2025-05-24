import os
import curses

from dotenv import load_dotenv
from utils.logger import logger
from project.csv.clean_csv import clean_csv

load_dotenv()
log = logger()

CSV_DIRECTORY = os.getenv('CSV_DIRECTORY')

def selectCSVFile(stdscr):
    curses.curs_set(0)
    
    try:
        files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith(".csv")]
    except FileNotFoundError:
        files = []

    options = files + ["Back"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"CSV Files in {CSV_DIRECTORY} (Use arrow keys to navigate, ENTER to select)")

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
        
def csvMenu(stdscr):
    selected_csv, num_rows = selectCSVFile(stdscr)
    if selected_csv:
        clean_csv(selected_csv, num_rows, stdscr)