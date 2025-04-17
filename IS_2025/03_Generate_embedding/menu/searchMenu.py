import curses
from project.qdrant.query import query_qdrant
from utils.tools.saveListTxt import saveListTxt

def askText(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the text to search (Press ENTER to confirm): ")
    
    curses.echo()  # Enable user input visibility
    stdscr.refresh()
    
    query = stdscr.getstr(1, 0, 100).decode("utf-8").strip()  # Read user input
    curses.noecho()  # Disable input visibility after entering the text

    return query  # Return the search query

def searchMenu(stdscr):
    stdscr.clear()
    
    query = askText(stdscr)  # Get the search query from the user
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"Searching for: {query}")
    
    # Call the query function with the provided query
    results = query_qdrant(query)
    saveListTxt(results, "./data/search/search.txt")  # Save results to a file
    
    stdscr.addstr(2, 0, "Search Results:")
    
    for idx, result in enumerate(results):
        stdscr.addstr(idx + 3, 2, f"Result {idx + 1}: {result}")
    
    stdscr.addstr(len(results) + 4, 0, "Press any key to go back...")
    stdscr.getch()  # Wait for user input before returning