import os
import time
import requests
import random
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://www.newadvent.org"
INDEX_URL = f"{BASE_URL}/fathers/"
SAVE_DIR = "augustine_texts"

# Create directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# User-Agent list to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
]

def sanitize_filename(filename):
    """Sanitize filename by replacing invalid characters."""
    return filename.replace("/", "_").replace(":", "").replace(",", "").replace(" ", "_")

def get_augustine_links():
    """Extracts links to all of Augustine's works from the index page."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(INDEX_URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    augustine_links = {}

    for link in soup.find_all("a", href=True):
        href = link["href"]
        title = link.text.strip()

        # Match all Augustine texts (fathers/11XX.htm to fathers/18XX.htm)
        if title and href.startswith("../fathers/") and "/fathers/1" in href:
            full_url = BASE_URL + href[2:]
            work_title = sanitize_filename(title.lower())
            augustine_links[work_title] = full_url

    return augustine_links

def get_chapter_links(work_url):
    """Extracts chapter links from a work's main page."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(work_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        chapter_links = {}

        for link in soup.find_all("a", href=True):
            href = link["href"]
            title = link.text.strip()

            # Extract all chapter links
            if href.startswith("../fathers/") and "BOOK" in title.upper():
                full_url = BASE_URL + href[2:]
                chapter_title = sanitize_filename(title.upper())
                chapter_links[chapter_title] = full_url

        return chapter_links

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching chapters for {work_url}: {e}")
        return {}

def download_content(work_title, chapter_title, chapter_url):
    """Downloads the text of a chapter or full work and saves it."""
    safe_work_title = sanitize_filename(work_title)
    safe_chapter_title = sanitize_filename(chapter_title)

    filename = os.path.join(SAVE_DIR, f"{safe_work_title}_{safe_chapter_title}.txt")

    # Skip if file already exists
    if os.path.exists(filename):
        print(f"   ✅ Skipping {filename} (already exists)")
        return filename

    retries = 3
    backoff_time = 5  # Initial wait time for backoff

    for attempt in range(retries):
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            response = requests.get(chapter_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            # Try extracting from the main content div
            content_div = soup.find("div", id="springfield2")

            # If springfield2 is empty, try getting all <p> tags in <body>
            if not content_div:
                content_div = soup.find("body")

            if not content_div:
                print(f"⚠️ No content found in {chapter_url}")
                return None

            text_content = "\n".join(p.get_text() for p in content_div.find_all("p"))

            # Save content to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text_content)

            return filename

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout on {chapter_url}. Retrying ({attempt+1}/{retries})...")
            time.sleep(backoff_time)
            backoff_time *= 2  # Exponential backoff

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error downloading {chapter_url}: {e}")
            return None

    print(f"❌ Failed to download {chapter_url} after {retries} attempts")
    return None

def scrape_augustine_works():
    """Main function to scrape and save all works in flat format."""
    print("Fetching list of works...")
    works = get_augustine_links()

    for work_title, work_url in tqdm(works.items(), desc="Scraping Works"):
        print(f"\n📖 Scraping: {work_title}")

        # Check if the main page has content
        has_main_content = download_content(work_title, "FULL_TEXT", work_url)

        chapter_links = get_chapter_links(work_url)

        if not chapter_links and not has_main_content:
            print(f"   ⚠️ No chapter links AND no content found for {work_title}, skipping...")
            continue

        for chapter_title, chapter_url in tqdm(chapter_links.items(), desc=f"Fetching {work_title} Chapters"):
            print(f"   📜 Downloading {chapter_title}...")
            file_path = download_content(work_title, chapter_title, chapter_url)
            if file_path:
                print(f"   ✅ Saved: {file_path}")

        # Avoid triggering rate limits by waiting before next request
        time.sleep(random.uniform(2, 4))

if __name__ == "__main__":
    scrape_augustine_works()