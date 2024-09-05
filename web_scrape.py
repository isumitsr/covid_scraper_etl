import requests
from bs4 import BeautifulSoup
import csv

#https://www.worldometers.info/coronavirus/

def scrape_table_data(url):

    try:

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if not table:
            print("No Table found on the given website")
            return None

        rows = table.find_all('tr')
        headers = [th.get_text(strip=True) for th in rows[0].find_all('th')] if rows[0].find_all('th') else None

        table_data = []
        for row in rows:
            cells = row.find_all('td')
            if cells:
                table_data.append([cell.get_text(strip=True) for cell in cells])

        return headers, table_data

    except requests.exceptions.RequestException as e:
        print(f"Oops! An error occured: {e}")
        return None, None
    
def save_to_csv(headers, data, filename="covid_worldometer_data.csv"):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer= csv.writer(file)

            if headers:
                writer.writerow(headers)
            writer.writerows(data)
        print(f"Data Saved succesfully to {filename}")
    except Exception as e:
        print(f"Oops! An error occured while saving data to csv: {e}")

if __name__=="__main__":

    url = input("Enter the website URL to scrape the data from: ")
    headers, table_data = scrape_table_data(url)

    if table_data:
        save_to_csv(headers, table_data)
    else:
        print("Failed to scrape any data from the website")
