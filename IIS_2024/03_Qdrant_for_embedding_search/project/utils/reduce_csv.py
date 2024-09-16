import csv

def reduce_csv(input_file, output_file, num_rows):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            for i, row in enumerate(reader):
                if i < num_rows:
                    writer.writerow(row)
                else:
                    break