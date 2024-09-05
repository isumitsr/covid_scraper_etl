import pandas as pd
import re

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

if __name__ == "__main__":
    input_file = "/Users/iamsumitsr/Desktop/Projects/Python/covid_scraper_etl/covid_worldometer_data.csv"
    output_file = "/Users/iamsumitsr/Desktop/Projects/Python/covid_scraper_etl/covidReport_clean.csv"
    
    clean_csv(input_file, output_file)
