
import time
import curses
import subprocess
import threading

from utils.logger import logger
from utils.tools.isHostRunning import isHostRunning

from menu.qdrant.searchMenu import searchMenu
from menu.qdrant.distanceMenu import distanceMenu
from menu.qdrant.searchMenu import searchParamsMenu
from menu.qdrant.searchMenu import processAllQueries

log = logger()

def checkQdrantStatus(stdscr, qdrantRunning):
    while True:
        new_status = isHostRunning("127.0.0.1", 6333)
        if new_status != qdrantRunning[0]:
            qdrantRunning[0] = new_status
        time.sleep(2)

def qdrantMenu(stdscr):
    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow text
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green (Running)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Red (Not Running)

    qdrantRunning = [isHostRunning("127.0.0.1", 6333)]

    status_thread = threading.Thread(target=checkQdrantStatus, args=(stdscr, qdrantRunning))
    status_thread.daemon = True
    status_thread.start()

    selected = 0

    while True:
        status_text = "Running" if qdrantRunning[0] else "Not Running"
        status_color = curses.color_pair(2) if qdrantRunning[0] else curses.color_pair(3)

        options = ["Stop", "Restart", "Load Data", "Search", "Search with Params", "Search all queries", "Back"] if qdrantRunning[0] else ["Start", "Back"]
        stdscr.clear()
        stdscr.addstr(0, 0, "Use arrow keys to navigate. Press ENTER to select.", curses.color_pair(1))
        stdscr.addstr(1, 0, f"Qdrant Status: {status_text}", status_color | curses.A_BOLD)

        for idx, option in enumerate(options):
            highlight = curses.A_BOLD if idx == selected else 0

            if option == 'Back':
                stdscr.addstr(idx + 3, 2, f"> {option}" if idx == selected else f"  {option}", curses.color_pair(3))
            else:
                stdscr.addstr(idx + 3, 2, f"> {option}" if idx == selected else f"  {option}")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == ord("\n"):
            if not handleOption(options[selected], stdscr):
                break

def handleOption(option: str, stdscr) -> bool:
    if option == "Start":
        log.info("Starting Qdrant")
        subprocess.run(["bash", "utils/scripts/startQdrant.sh"])
        time.sleep(5)
    elif option == "Stop":
        log.info("Stopping Qdrant")
        subprocess.run(["bash", "utils/scripts/stopQdrant.sh"])
    elif option == "Restart":
        log.info("Restarting Qdrant")
        subprocess.run(["bash", "utils/scripts/restartQdrant.sh"])
    elif option == "Load Data":
        log.info("Loading Data into Qdrant")
        distanceMenu(stdscr)
    elif option == "Search":
        log.info("Searching in Qdrant")
        searchMenu(stdscr)
    elif option == "Search with Params":
        log.info("Searching in Qdrant with Params")
        searchParamsMenu(stdscr)
    elif option == "Search all queries":
        log.info("Searching all queries in Qdrant")
        processAllQueries(stdscr)
    elif option == "Back":
        return False
    return True