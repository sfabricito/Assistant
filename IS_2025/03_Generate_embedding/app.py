import curses

from utils.shell import model_shell, csv_shell
from utils.csv.clean_csv import clean_csv

from utils.logger import logger
from utils.embedding.app import generate_embeddings

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
            stdscr.refresh()
            curses.napms(200)

            if options[selected] == "Exit":
                break
            elif options[selected] == "Clean CSV":
                selected_csv, num_rows = csv_shell(stdscr)
                if selected_csv:
                    clean_csv(selected_csv, num_rows, stdscr)
                stdscr.clear()
                stdscr.refresh()
                curses.doupdate()
            elif options[selected] == "Generate Embeddings":
                selected_model, selected_parquet = model_shell(stdscr)
                if selected_model and selected_parquet:
                    log.info(f'Selected model: {selected_model} {selected_parquet}')
                    generate_embeddings(selected_model, selected_parquet, stdscr)
                    log.info('after generate embeddings')
                stdscr.clear()
                stdscr.refresh()

curses.wrapper(interactive_shell)
