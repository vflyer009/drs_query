import csv
import re

def save_table_to_csv(api_response_content, csv_file_path):
    # Extract the lines of the table
    table_lines = re.findall(r'\|.*?\|', api_response_content)

    # Process the lines into a list of rows
    table_rows = [line.strip('|').split('|') for line in table_lines]

    # Clean up extra spaces
    table_rows = [[cell.strip() for cell in row] for row in table_rows]

    # Save the table as a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(table_rows)