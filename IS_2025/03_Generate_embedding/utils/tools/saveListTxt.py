def saveListTxt(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for item in data:
            file.write(f"{item}\n")