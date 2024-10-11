import requests
import csv
import io

# URL of the dataset
url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/trees-with-species-and-dimensions-urban-forest/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true"

# Send GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Decode the content to a string
    content = response.content.decode('utf-8')
    
    # Use io.StringIO to treat the string as a file
    csv_file = io.StringIO(content)
    
    # Read the CSV content
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    # Write the CSV content to a properly formatted CSV file
    with open("trees_with_species_and_dimensions.csv", "w", newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for row in csv_reader:
            csv_writer.writerow(row)
    
    print("CSV file has been saved successfully.")
else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")