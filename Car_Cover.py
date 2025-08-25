import requests
from bs4 import BeautifulSoup
import csv

def scrape_olx_car_cover(output_file='car_cover_results.csv'):
    url = "https://www.olx.in/items/q-car-cover"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find("ul", {"data-aut-id": "itemsList1"})
    if not listings:
        print("No listings found on the page.")
        return

    results = []
    for item in listings.find_all("li"):
        title_tag = item.find("span", {"data-aut-id": "itemTitle"})
        price_tag = item.find("span", {"data-aut-id": "itemPrice"})
        location_tag = item.find("span", {"data-aut-id": "item-location"})
        link_tag = item.find("a")

        if not (title_tag and price_tag and location_tag and link_tag):
            continue

        title = title_tag.text.strip()
        price = price_tag.text.strip()
        location = location_tag.text.strip()
        link = "https://www.olx.in" + link_tag.get("href", "")

        results.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Link": link
        })

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Location", "Link"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Scraping complete. {len(results)} listings saved to '{output_file}'.")

if __name__ == "__main__":
    scrape_olx_car_cover()
