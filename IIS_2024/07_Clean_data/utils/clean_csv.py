import csv
import random

def clean_csv(input_file, output_file, num_rows=100):
    with open(input_file, mode='r', newline='', encoding='ISO-8859-1') as infile:
        reader = list(csv.reader(infile))
        header = reader[0]  # Save the header
        data = reader[1:]  # The rest is the data
        
        # Randomly sample the specified number of rows
        selected_rows = random.sample(data, num_rows)

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            
            # Write the header first
            writer.writerow(["id", "date", "location", "attack_type", "target_type", "corporation", "target", "orchestrating_group", "weapon", "deceased", "notes", "scite1", "scite2", "scite3"])

            # Process and write the selected rows
            for row in selected_rows:
                row_to_insert = format_row(row)
                if row_to_insert:
                    writer.writerow(row_to_insert)


def format_row(row):
    result = [
        row[0],  # id
        f"{row[1]}-{row[2]}-{row[3]}",  # date
        f"{row[8]}, {row[11]}, {row[12]}",  # location
        row[29],  # attack type
        f"{row[35]}, {row[37]}",  # type_target
        row[38],  # corporation
        row[39],  # target
        row[58],  # orchestrating_group
    ]

    weapon = "unknown"
    if row[82] or row[84]:
        weapon = f"{row[82]}, {row[84]}" if row[82] and row[84] else row[82] or row[84]
    result.append(weapon)

    result.append(row[98] if row[98] else 'unknown')

    additional_info = [row[idx] if row[idx] else 'unknown' for idx in [125, 126, 127, 128]]
    if all(info == 'unknown' for info in additional_info):
        return []
    
    result.extend(additional_info)

    return result
