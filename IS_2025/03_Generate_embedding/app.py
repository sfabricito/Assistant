import os
import curses

from menu.qdrant import qdrantMenu

from utils.shell import model_shell, csv_shell
from project.csv.clean_csv import clean_csv

from utils.logger import logger
from project.embedding.app import generate_embeddings

log = logger()

def interactive_shell(stdscr):
    curses.curs_set(0)
    options = ["Clean CSV", "Generate Embeddings", "Qdrant", "Exit"]
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
            if not handleOption(options[selected], stdscr):
                break
            stdscr.clear()
            stdscr.refresh()


def handleOption(option: str, stdscr) -> bool:
    if option == "Clean CSV":
        log.info("Selected menu: Clean CSV")
        selected_csv, num_rows = csv_shell(stdscr)
        if selected_csv:
            clean_csv(selected_csv, num_rows, stdscr)

    elif option == "Generate Embeddings":
        log.info("Selected menu: Generate Embeddings")
        selected_model, selected_parquet = model_shell(stdscr)
        if selected_model and selected_parquet:
            generate_embeddings(selected_model, selected_parquet, stdscr)
    elif option == "Qdrant":
        log.info("Loading Data into Qdrant")
        qdrantMenu(stdscr)
    elif option == "Exit":
        return False
    return True


if __name__=="__main__":
    curses.wrapper(interactive_shell)