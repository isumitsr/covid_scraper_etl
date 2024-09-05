import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import pandas as pd
import re

#https://www.worldometers.info/coronavirus/

def remove_special_characters(text):
    if isinstance(text, str):
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def clean_csv(input_file, output_file):
    # Read the CSV file without using the header row
    df = pd.read_csv(input_file, header=None)
    
    # Drop the first column (index 0) which is '#'
    df = df.drop(columns=[0])
    
    # Find the start index where the actual data starts (i.e., where rows contain a numeric value)
    start_index = df[df[1].astype(str).str.contains('USA', na=False)].index[0]
    
    # Extract the data starting from the identified start_index
    cleaned_df = df.iloc[start_index:]
    
    # Rename columns to avoid issues with unnamed columns
    cleaned_df.columns = ['CountryOther', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 
                          'NewRecovered', 'ActiveCases', 'SeriousCritical', 'TotCases1Mpop', 'Deaths1Mpop', 
                          'TotalTests', 'Tests1Mpop', 'Population', 'Continent', 'CaseeveryXppl', 
                          'DeatheveryXppl', 'TesteveryXppl', 'NewCases1Mpop', 'NewDeaths1Mpop', 
                          'ActiveCases1Mpop']

    # Remove special characters from the DataFrame
    cleaned_df = cleaned_df.apply(lambda x: x.apply(remove_special_characters))
    
    # Save the cleaned DataFrame
    cleaned_df.to_csv(output_file, index=False)
    
    print(f"Cleaned Data saved to {output_file}")


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
    input_file = "/Users/iamsumitsr/Desktop/Projects/Python/covid_scraper_etl/covid_worldometer_data.csv"
    output_file = "/Users/iamsumitsr/Desktop/Projects/Python/covid_scraper_etl/covidReport_clean.csv"

    url = input("Enter the website URL to scrape the data from: ")
    headers, table_data = scrape_table_data(url)

    if table_data:
        save_to_csv(headers, table_data)
    else:
        print("Failed to scrape any data from the website")
        
    clean_csv(input_file, output_file)

