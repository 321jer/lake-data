import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
import json
import re
from bs4 import BeautifulSoup

try:
    # Step 1: Load the page
    page = requests.get('https://wre-rapps.utah.gov/Reservoir/', verify=False)
    page.raise_for_status()
    print("Page fetched successfully")

    # Step 2: Parse HTML
    soup = BeautifulSoup(page.content, 'html.parser')

    # Step 3: Find download button
    btn = soup.find('a', href=re.compile(r'/Reservoir/session/.+/download/downloadData'))
    if not btn:
        raise ValueError("Download button not found on the page")

    csv_url = 'https://wre-rapps.utah.gov' + btn['href']
    print("CSV URL found:", csv_url)

    # Step 4: Download CSV
    csv_data = requests.get(csv_url, verify=False)
    csv_data.raise_for_status()

    with open("kenslake_temp.csv", "wb") as f:
        f.write(csv_data.content)

    # Step 5: Read and clean the CSV
    df = pd.read_csv("kenslake_temp.csv")
    df.columns = df.columns.str.strip()

    # Get the last row (most recent data)
    latest = df.iloc[-1]
    date = latest['Date']
    storage = latest['Storage (acft)']
    capacity = latest.get('Capacity (acft)', None)

    # Save to JSON
    output = {
        "date": date,
        "storage_acft": storage,
        "capacity_acft": capacity
    }

    with open("kenslake.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Data saved to kenslake.json:", output)

except Exception as e:
    print("ERROR:", e)
    raise

