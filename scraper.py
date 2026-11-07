import json
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {
    "User-Agent": "InternCircle-learning-project (student scraper; educational use)"
}
TIMEOUT = 10
REQUEST_DELAY_SECONDS = 1
MAX_PAGES = 10  # The practice site has a finite set of pages.


def extract_quotes(html):
    """Extract quote text, author, and tags from one HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for quote_element in soup.select("div.quote"):
        text_element = quote_element.select_one("span.text")
        author_element = quote_element.select_one("small.author")

        # Check selectors before reading text, as required by the learner guide.
        if text_element is None or author_element is None:
            continue

        results.append({
            "text": text_element.get_text(strip=True),
            "author": author_element.get_text(strip=True),
            "tags": [
                tag.get_text(strip=True)
                for tag in quote_element.select("a.tag")
            ],
        })

    next_link = soup.select_one("li.next a")
    next_url = urljoin(BASE_URL, next_link.get("href")) if next_link else None
    return results, next_url


def scrape_quotes():
    """Fetch the practice site's pages politely and return extracted quotes."""
    current_url = BASE_URL
    all_quotes = []
    visited_urls = set()
    page_count = 0

    session = requests.Session()
    session.headers.update(HEADERS)

    while current_url and page_count < MAX_PAGES:
        if current_url in visited_urls:
            print("A previously visited page was detected; stopping pagination.")
            break

        visited_urls.add(current_url)
        page_count += 1
        print(f"Fetching page {page_count}: {current_url}")

        try:
            response = session.get(current_url, timeout=TIMEOUT)
            response.raise_for_status()
        except RequestException as error:
            print(f"Request failed: {error}")
            if not all_quotes:
                raise RuntimeError(
                    "Could not retrieve the practice website. Check your internet "
                    "connection and try again."
                ) from error
            print("Keeping the quotes collected from earlier pages.")
            break

        page_quotes, next_url = extract_quotes(response.text)
        all_quotes.extend(page_quotes)
        print(f"  Found {len(page_quotes)} quotes on this page.")

        current_url = next_url
        if current_url:
            time.sleep(REQUEST_DELAY_SECONDS)

    return all_quotes, page_count


def save_json(quotes, output_path="quotes.json"):
    """Save extracted records as readable UTF-8 JSON."""
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)


def save_text(quotes, output_path="quotes.txt"):
    """Save extracted records in a human-readable text format."""
    with open(output_path, "w", encoding="utf-8") as file:
        for number, quote in enumerate(quotes, start=1):
            file.write(f"{number}. {quote['text']}\n")
            file.write(f"   Author: {quote['author']}\n")
            file.write(f"   Tags: {', '.join(quote['tags']) or 'None'}\n\n")


def print_summary(quotes, page_count):
    """Print quote count, most quoted author, and most common tag."""
    print("\n========== SCRAPING SUMMARY ==========")
    print(f"Pages visited : {page_count}")
    print(f"Quotes found  : {len(quotes)}")

    if not quotes:
        print("No quotes were extracted.")
        return

    author_counts = Counter(quote["author"] for quote in quotes)
    tag_counts = Counter(
        tag for quote in quotes for tag in quote["tags"]
    )

    author, author_total = author_counts.most_common(1)[0]
    print(f"Most quoted author: {author} ({author_total} quotes)")

    if tag_counts:
        tag, tag_total = tag_counts.most_common(1)[0]
        print(f"Most common tag   : {tag} ({tag_total} uses)")
    else:
        print("Most common tag   : No tags found")


def main():
    print("======================================")
    print("       WEB SCRAPER: QUOTES")
    print("======================================")
    print(f"Allowed practice source: {BASE_URL}")
    print("This scraper waits one second between page requests.")

    try:
        quotes, page_count = scrape_quotes()
    except RuntimeError as error:
        print(f"\nScraping stopped: {error}")
        return

    try:
        save_json(quotes)
        save_text(quotes)
    except OSError as error:
        print(f"Could not save output files: {error}")
        return

    print(f"\nSaved {len(quotes)} records to quotes.json and quotes.txt.")
    print_summary(quotes, page_count)


if __name__ == "__main__":
    main()
