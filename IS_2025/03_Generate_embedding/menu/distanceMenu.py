import curses

from utils.tools.findFiles import findFiles
from menu.loadDataMenu import loadDataMenu

def distanceMenu(stdscr) -> bool:
    options = ['Cosine Similiarity', 'Euclidean Distance', 'Dot Product', 'Back']
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Type of distance (Use arrow keys to navigate, ENTER to select)")

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
                loadDataMenu(stdscr, options[selected])