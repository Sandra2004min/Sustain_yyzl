import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Load the JSON file containing article links
with open("GZNYJT_News.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

# Function to scrape article content
def scrape_article_content(article):
    try:
        title = article["title"]
        link = article["link"]
        date = article["date"]
        
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Locate the main content
        content_div = soup.find("div", class_="artcontent", id="zoom")
        if not content_div:
            return {
                "title": title,
                "link": link,
                "date": date,
                "content": "Content not found"
            }

        # Check if content is primarily in span or p tags
        span_tags = content_div.find_all("span")
        if span_tags:  # Case 1: Use span tags
            content = []
            for span in span_tags:
                if span.string:  # Only include textual content
                    content.append(span.string.strip())
            return {
                "title": title,
                "link": link,
                "date": date,
                "content": "\n".join(content)
            }

        # Case 2: Use p tags
        p_tags = content_div.find_all("p")
        if p_tags:
            content = []
            for p in p_tags:
                if p.string:  # Only include textual content
                    content.append(p.string.strip())
            return {
                "title": title,
                "link": link,
                "date": date,
                "content": "\n".join(content)
            }

        return {
            "title": title,
            "link": link,
            "date": date,
            "content": "No valid content found"
        }
    except Exception as e:
        return {
            "title": article["title"],
            "link": article["link"],
            "date": article["date"],
            "content": f"Error: {str(e)}"
        }

# Multi-threaded scraping
article_data = []
with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
    futures = list(tqdm(executor.map(scrape_article_content, articles), total=len(articles), desc="Scraping Articles"))

# Collect results
article_data = list(futures)

# Save the results to a JSON file
output_file = "GZNYJT_Articles.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(article_data, file, ensure_ascii=False, indent=4)

print(f"Article data saved to {output_file}")
