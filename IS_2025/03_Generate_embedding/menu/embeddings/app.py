import os
import re
import curses

from dotenv import load_dotenv
from utils.logger import logger
from utils.tools.models import getModelNames
from project.embedding.app import generate_embeddings

load_dotenv()

CLEAN_DATA_DIRECTORY = os.getenv('CLEAN_DATA_DIRECTORY')

log = logger()

def selectEmbeddingModelMenu(stdscr):
    curses.curs_set(0)
    options = getModelNames()
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
            selected_parquet = selectParquetMenu(stdscr)
            if selected_parquet is None:
                continue
            return options[selected], selected_parquet
        
def selectParquetMenu(stdscr):
    curses.curs_set(0)
    
    def natural_sort_key(filename):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', filename)]

    try:
        files = sorted(
            [f for f in os.listdir(CLEAN_DATA_DIRECTORY) if f.endswith(".parquet")],
            key=natural_sort_key
        )
    except FileNotFoundError:
        files = []

    options = files + ["Back"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Parquet Files in {CLEAN_DATA_DIRECTORY} (Use arrow keys to navigate, ENTER to select)")

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
        
def embeddingMenu(stdscr):
    selectedModel, selectedParquet = selectEmbeddingModelMenu(stdscr)
    if selectedModel and selectedParquet:
        generate_embeddings(selectedModel, selectedParquet, stdscr)