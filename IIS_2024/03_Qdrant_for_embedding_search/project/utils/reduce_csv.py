import csv

def save_limited_rows(input_file, output_file, num_rows):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            for i, row in enumerate(reader):
                if i < num_rows:
                    writer.writerow(row)
                else:
                    break

input_file = './data/vector_database_wikipedia_articles_embedded.csv'
output_file = './data/small_vector_database_wikipedia_articles_embedded.csv'
num_rows = 1500

save_limited_rows(input_file, output_file, num_rows)

print(f"Saved the first {num_rows} rows from '{input_file}' to '{output_file}'.")
