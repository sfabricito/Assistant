import curses

from utils.logger import logger
from menu.csv.app import csvMenu
from menu.qdrant.app import qdrantMenu
from menu.embeddings.app import embeddingMenu

log = logger()

def menu(stdscr):
    log.info("Starting Menu")
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
        csvMenu(stdscr)

    elif option == "Generate Embeddings":
        log.info("Selected menu: Generate Embeddings")
        embeddingMenu(stdscr)
    elif option == "Qdrant":
        log.info("Selected menu: Qdrant")
        qdrantMenu(stdscr)
    elif option == "Exit":
        return False
    return True