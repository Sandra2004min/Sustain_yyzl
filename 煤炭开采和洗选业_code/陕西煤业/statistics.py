import json

def count_empty_content(json_file):
    """Count articles with empty content in the JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return

    empty_count = sum(1 for article in articles if not article.get('content'))
    
    print(f"Number of articles with empty content: {empty_count}")

# Usage
json_file = "articles_with_content.json"  # JSON file to analyze
count_empty_content(json_file)
