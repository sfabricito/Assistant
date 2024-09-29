import csv

def clean_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='ISO-8859-1') as infile:
        reader = csv.reader(infile)
        
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            for i, row in enumerate(reader):
                if i == 0:
                    row_to_insert = ["id", "date", "location", "attack_type", "target_type", "corporation", "target", "orchestrating_group", "weapon", "deceased", "notes", "scite1", "scite2", "scite3"]
                else:
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
    result.append(row[98])  # decease

    if all(not row[idx] for idx in [125, 126, 127, 128]):
        return []

    result.extend([row[125], row[126], row[127], row[128]])

    return result
