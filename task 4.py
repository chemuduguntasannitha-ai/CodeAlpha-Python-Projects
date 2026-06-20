"""
CodeAlpha Data Analytics Internship - Task 4
Web Scraping
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping project - CodeAlpha internship)"}

os.makedirs("outputs", exist_ok=True)

def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    quotes_data = []
    for quote_block in soup.select("div.quote"):
        text = quote_block.select_one("span.text").get_text(strip=True)
        author = quote_block.select_one("small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_block.select("div.tags a.tag")]
        quotes_data.append({"quote": text, "author": author, "tags": ", ".join(tags)})

    return quotes_data

def get_next_page_url(soup):
    next_link = soup.select_one("li.next a")
    return BASE_URL + next_link["href"] if next_link else None

def scrape_all_pages(start_url, max_pages=10):
    all_quotes = []
    url = start_url
    page_count = 0

    while url and page_count < max_pages:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        all_quotes.extend(scrape_page(url))
        url = get_next_page_url(soup)
        page_count += 1
        time.sleep(1)

    return pd.DataFrame(all_quotes)

if __name__ == "__main__":
    df = scrape_all_pages(BASE_URL, max_pages=10)
    print(f"Scraped {len(df)} quotes total.")
    print(df.head(10).to_string(index=False))

    df.to_csv("outputs/quotes_scraped.csv", index=False)
    print("Saved to outputs/quotes_scraped.csv")

    print("Top 5 authors:")
    print(df["author"].value_counts().head(5))

    all_tags = df["tags"].str.split(", ").explode()
    print("Top 10 tags:")
    print(all_tags.value_counts().head(10))
