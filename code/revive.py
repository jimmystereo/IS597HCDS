import json
import csv

# Load the JSON file
with open('news/arch/abcnews.json', 'r') as json_file:
    data = json.load(json_file)


# Open a CSV file to write the data with tab separator
with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=data[0].keys(), delimiter='\t')
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows