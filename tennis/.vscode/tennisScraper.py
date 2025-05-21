import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of Grand Slam tournament URLs (example: ATP or Grand Slam websites)
BASE_URLS = {
    "Australian Open": "https://ausopen.com/history/honour-roll/mens-singles",
    "French Open": "https://www.rolandgarros.com/en-us/champions-wall",
    "Wimbledon": "https://www.wimbledon.com/en_GB/draws_archive/events.html",
    "US Open": "https://www.usopen.org/en_US/visit/history/mschamps.html"
}

# Define the years to scrape (last 10 years)
YEARS = list(range(2014, 2025))

def scrape_us_open():
    """
    Scrapes the US Open data from the given URL.
    """
    url = BASE_URLS["US Open"]
    print(f"Fetching URL: {url}")  # Debugging URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for US Open: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(f"HTML content for US Open: {soup.prettify()}")  # Debugging HTML content

    # Find all rows containing match data
    rows = soup.find_all("div", class_="pl-row")
    print(f"Found {len(rows)} rows for US Open.")  # Debugging number of rows

    data = []
    for row in rows:
        try:
            # Extract the year
            year = row.find("div", class_="playoff_reg_register").text.strip()

            # Extract the champion
            champion_div = row.find("div", class_="playoff_reg_city", text=lambda x: x and "Champion:" in x)
            champion = champion_div.text.replace("Champion:", "").strip()

            # Append the extracted data
            data.append({
                "Year": year,
                "Champion": champion
            })
        except AttributeError:
            print(f"Skipping row due to missing data: {row}")
            continue

    return data

#------------------------------------------------------------------------------------------------

def scrape_aus_open():
    """
    Scrapes the Australian Open data from the given HTML structure.
    """
    url = BASE_URLS["Australian Open"]
    print(f"Fetching URL: {url}")  # Debugging URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for Australian Open: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(f"HTML content for Australian Open: {soup.prettify()}")  # Debugging HTML content

    # Find the table containing the data
    table = soup.find("table", align="left", border="1")
    if not table:
        print("No table found for Australian Open data.")
        return []

    # Find all rows within the table body
    rows = table.find("tbody").find_all("tr")
    print(f"Found {len(rows)} rows for Australian Open.")  # Debugging number of rows

    data = []
    for row in rows:
        try:
            # Extract the cells from the row
            cells = row.find_all("td")
            year = cells[0].text.strip()
            champion = cells[1].text.strip()

            # Append the extracted data
            data.append({
                "Year": year,
                "Champion": champion
            })
        except (IndexError, AttributeError) as e:
            print(f"Skipping row due to missing or malformed data: {row}")
            continue

    return data

#---------------------------------------------------------------------------------------------------------------------------

def scrape_grand_slam(tournament, year):
    """
    Scrapes match data for a given tournament and year.
    """
    url = BASE_URLS[tournament]  # Using static URLs for now
    print(f"Fetching URL: {url}")  # Debugging URL
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {tournament} {year}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(f"HTML content for {tournament} {year}: {soup.prettify()}")  # Debugging HTML content

    # Update this based on the actual structure of the website
    match_rows = soup.select(".scores-draw-entry")  # Example selector
    print(f"Found {len(match_rows)} match rows for {tournament} {year}")  # Debugging number of rows

    data = []

    for match in match_rows:
        try:
            player1 = match.select_one(".player-left .player-name").text.strip()
            player2 = match.select_one(".player-right .player-name").text.strip()
            score = match.select_one(".scores-draw-entry-score").text.strip()
            round_ = match.select_one(".scores-draw-entry-round").text.strip()
            data.append({
                "Year": year,
                "Tournament": tournament,
                "Player1": player1,
                "Player2": player2,
                "Score": score,
                "Round": round_,
            })
        except AttributeError:
            print(f"Skipping row due to missing data: {match}")  # Debugging missing data
            continue

    return data

def scrape_all_data():
    """
    Scrapes data for all Grand Slams and years.
    """
    all_matches = []

    for tournament, base_url in BASE_URLS.items():
        for year in YEARS:
            print(f"Scraping {tournament} {year}...")
            matches = scrape_grand_slam(tournament, year)
            all_matches.extend(matches)

    return all_matches

def save_to_csv(data, filename="grand_slam_matches.csv"):
    """
    Saves the scraped data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Scrape the data
    scraped_data = scrape_all_data()

    # Save to CSV
    if scraped_data:
        save_to_csv(scraped_data)
    else:
        print("No data scraped.")