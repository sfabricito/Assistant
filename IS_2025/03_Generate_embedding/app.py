import curses
from menu.app import menu

if __name__=="__main__":
    curses.wrapper(menu)