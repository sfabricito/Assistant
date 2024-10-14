import time
from utils.generate_embeddings import generate_embeddings
from utils.read_file import read_file
from utils.store_embeddings import store_embeddings

FILENAME = './data/globalTerrorism20000.parquet'

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

start_time = time.perf_counter()
store_embeddings(FILENAME)

data = read_file(FILENAME)
total_rows = len(data)
end_time = time.perf_counter()
elapsed_time = end_time - start_time
average_time_per_row = elapsed_time / total_rows

print(f"Program executed in {format_time(elapsed_time)}")
print(f"Start time: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
print(f"Finish time: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
print(f"Average time per row in seconds: {round(average_time_per_row, 3)}")