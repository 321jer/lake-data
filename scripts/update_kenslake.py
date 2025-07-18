import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import json
from bs4 import BeautifulSoup

try:
    page = requests.get('https://wre-rapps.utah.gov/Reservoir/', verify=False)
    page.raise_for_status()
    print("Page fetched successfully")

    soup = BeautifulSoup(page.text, 'html.parser')
    btn = soup.select_one("a[href*='downloadData']")
    csv_url = 'https://wre-rapps.utah.gov' + btn['href']
    print(f"CSV URL found: {csv_url}")

    df = pd.read_csv(csv_url)
    print("CSV loaded, columns:", df.columns.tolist())

    row = df[df['Reservoir'].str.contains("Ken's Lake", na=False)]
    if row.empty:
        raise ValueError("No row found for Ken's Lake")
    row = row.iloc[0]

    output = {
        'capacity': float(row['Capacity (AF)']),
        'current': float(row['Current Storage (AF)']),
        'percent': float(row['% Full']),
        'date': row['Data Date']
    }

    with open('kenslake_data.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("✅ Ken's Lake data saved to kenslake_data.json")

except Exception as e:
    print("ERROR:", e)
    raise
