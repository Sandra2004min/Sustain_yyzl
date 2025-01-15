import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm  # For progress bar

# Base URL
base_url = "https://www.gznyjt.cn/channels/c14/c14_{}.html"

# Result list
news_list = []

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate news list items
    news_section = soup.find('div', class_='news_list')
    if news_section:
        articles = news_section.find_all('li')
        for article in articles:
            # Extract title
            title = article.find('p', class_='name').text.strip()
            
            # Extract link and complete URL
            link = article.find('a')['href']
            full_link = "https://www.gznyjt.cn/" + link
            
            # Extract date
            date = article.find('p', class_='time').text.strip()
            
            # Append to list
            news_list.append({
                "title": title,
                "link": full_link,
                "date": date
            })

# Loop through pages with progress bar
start_page = 1
end_page = 493  # Adjust this range as needed
for page in tqdm(range(start_page, end_page + 1), desc="Scraping Pages"):
    scrape_page(page)

# Save results to a JSON file
json_file_path = "GZNYJT_News.json"
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(news_list, json_file, ensure_ascii=False, indent=4)

print(f"News data saved to {json_file_path}")
