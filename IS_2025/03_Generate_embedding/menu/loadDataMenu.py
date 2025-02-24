import curses

from utils.tools.findFiles import findFiles
from project.qdrant.app import main

def loadDataMenu(stdscr) -> bool:
    directory = 'data/embedding'
    files = findFiles(directory, 'parquet')

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
            if options[selected] == "Back":
                return False
            else:
                main(options[selected])