import requests
from bs4 import BeautifulSoup
import json

# Base URL to scrape
base_url = "https://www.luanhn.com/channel/newsCenter/"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
}

# List to store all articles from all pages
all_articles = []

# Loop through pages 1 to 13
for page_num in range(1, 14):
    # Construct the URL for the current page
    url = f"{base_url}{page_num}"

    # Send a GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the container holding all articles
        articles_container = soup.find("div", class_="col-lg-8")

        # Extract all article elements
        articles = articles_container.find_all("li", class_="media")

        # Loop through each article and extract information
        for article in articles:
            # Find the title and link
            title_tag = article.find("a", class_="cm-link")
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag.get("href")
            else:
                title = None
                link = None

            # Find the publication date
            date_tag = article.find("div", class_="float-right")
            if date_tag:
                publication_date = date_tag.text.strip()
            else:
                publication_date = None

            # Append the data to the list
            all_articles.append({
                "title": title,
                "link": link,
                "publication_date": publication_date
            })

    else:
        print(f"Failed to retrieve the webpage for page {page_num}. Status code: {response.status_code}")

# Save the data to a JSON file
with open("articles.json", "w", encoding="utf-8") as json_file:
    json.dump(all_articles, json_file, ensure_ascii=False, indent=4)

print("Data saved to articles.json")
