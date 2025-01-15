import json
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a session with retries and SSL verification disabled."""
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.verify = False  # Disable SSL certificate verification
    return session

def extract_wechat_content(url, session):
    """Extract content from a WeChat article."""
    response = session.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='rich_media_content')
    if content:
        paragraphs = content.find_all(['span', 'p'])
        text = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        return '\n'.join(text)
    return None

def extract_dyny_content(url, session):
    """Extract content from a dyny article."""
    response = session.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='news_info')
    if content:
        paragraphs = content.find_all('p')
        text = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        return '\n'.join(text)
    return None

def main():
    # Create a requests session
    session = create_session()

    # Load articles.json
    with open('articles.json', 'r', encoding='utf-8') as file:
        articles = json.load(file)
    
    results = []

    for article in articles:
        title = article.get('title')
        link = article.get('url')
        publish_time = article.get('publish_time')
        print(title)
        content = None

        try:
            if 'mp.weixin.qq.com' in link:
                content = extract_wechat_content(link, session)
            elif 'dyny.hnecgc.com.cn' in link:
                content = extract_dyny_content(link, session)
            
            if content:
                results.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'publish_time': publish_time
                })
        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Save to a new JSON file
    with open('articles_with_content.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
