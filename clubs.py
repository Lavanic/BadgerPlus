import csv
input_filename = "clubs.txt"
output_filename = "clubs_data.csv"
data = []
with open(input_filename, "r", encoding="utf-8") as file:
    for line in file:
        club_name, category = map(str.strip, line.split(",", 1))
        data.append((club_name, category))
with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Club Name", "Category"])
    writer.writerows(data)