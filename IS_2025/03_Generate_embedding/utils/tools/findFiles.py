import os
import re

from utils.logger import logger

log = logger()

def findFiles(directory, extension):
    try:
        files = [f for f in os.listdir(directory) if f.endswith(f'.{extension}')]
        sorted_files = sorted(files, key=customSortKey)
        log.info('files found')
        return sorted_files
    except FileNotFoundError:
        return []

def customSortKey(filename):
    # Extracting number and model
    match = re.match(r'globalTerrorism_(\d+)(?:_([a-zA-Z0-9\-]+))?', filename)
    
    if match:
        number = int(match.group(1))  # Extracted number
        model = match.group(2) or ""  # Extracted model (or empty if not present)
    else:
        number = float('inf')  # Put non-matching filenames at the end
        model = ""

    return (model, number)