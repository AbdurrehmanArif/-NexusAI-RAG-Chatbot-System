import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List
import time


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# Tags to completely remove before text extraction
REMOVE_TAGS = [
    "script", "style", "noscript", "nav", "header", "footer",
    "aside", "form", "button", "input", "iframe", "svg",
    "advertisement", "ads",
]


def _clean_soup(soup: BeautifulSoup) -> str:
    """Remove unwanted tags and return clean text."""
    for tag in soup.find_all(REMOVE_TAGS):
        tag.decompose()

    # Extract only main content if available
    main = soup.find("main") or soup.find("article") or soup.find("body")
    if main:
        text = main.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    # Clean up blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def scrape_page(url: str) -> str | None:
    """Scrape a single page and return clean text."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        return _clean_soup(soup)
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None


def get_internal_links(base_url: str, max_links: int = 10) -> List[str]:
    """Collect internal links from the base page (up to max_links)."""
    try:
        resp = requests.get(base_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        domain = urlparse(base_url).netloc
        links = set()
        links.add(base_url)

        for a_tag in soup.find_all("a", href=True):
            href = urljoin(base_url, a_tag["href"])
            parsed = urlparse(href)
            # Only same-domain, no fragments, no query-heavy URLs
            if (
                parsed.netloc == domain
                and not parsed.fragment
                and parsed.scheme in ("http", "https")
                and len(parsed.query) < 50
            ):
                links.add(href)
            if len(links) >= max_links:
                break

        return list(links)
    except Exception as e:
        print(f"❌ Could not collect links from {base_url}: {e}")
        return [base_url]


def scrape_website(url: str, max_pages: int = 10) -> List[dict]:
    """
    Scrape up to max_pages pages of a website.
    Returns list of {"url": ..., "content": ...} dicts.
    """
    pages = []
    links = get_internal_links(url, max_links=max_pages)

    for link in links:
        print(f"🔍 Scraping: {link}")
        content = scrape_page(link)
        if content and len(content) > 100:  # skip near-empty pages
            pages.append({"url": link, "content": content})
        time.sleep(0.5)  # polite delay

    return pages