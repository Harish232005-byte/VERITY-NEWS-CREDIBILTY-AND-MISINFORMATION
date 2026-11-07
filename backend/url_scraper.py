"""
News URL Article Scraper and Metadata Extractor.
Extracts title, domain, author, publish date, and clean text body using BeautifulSoup.
"""

import re
import urllib.parse
import requests
from bs4 import BeautifulSoup


def extract_domain(url: str) -> str:
    """Extract clean domain name from URL (e.g. 'bbc.com')."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return "unknown"


def scrape_article_from_url(url: str) -> dict:
    """Fetch article content, title, and metadata from URL."""
    domain = extract_domain(url)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve URL ({str(e)})",
            "domain": domain,
            "url": url
        }

    soup = BeautifulSoup(html, "html.parser")

    # Clean out non-content elements
    for el in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg", "form"]):
        el.decompose()

    # 1. Title Extraction
    title = ""
    # OpenGraph title
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    elif soup.title and soup.title.string:
        title = soup.title.string.strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text().strip()

    # Clean title suffixes like ' - BBC News' or ' | Reuters'
    title = re.sub(r'\s*[-|–]\s*.*$', '', title)

    # 2. Author & Date Extraction
    author = "Unknown Journalist / Agency"
    author_meta = soup.find("meta", {"name": re.compile(r"author", re.I)}) or soup.find("meta", property="article:author")
    if author_meta and author_meta.get("content"):
        author = author_meta["content"].strip()

    publish_date = "Recently Published"
    date_meta = soup.find("meta", property="article:published_time") or soup.find("meta", {"name": re.compile(r"date|pubdate", re.I)})
    if date_meta and date_meta.get("content"):
        publish_date = date_meta["content"].strip()[:10]

    # 3. Main Body Text Extraction
    # Look for standard article container tags
    article_tag = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"article-body|story-body|content__article|post-content", re.I))

    paragraphs = []
    target_container = article_tag if article_tag else soup.body

    if target_container:
        for p in target_container.find_all("p"):
            text = p.get_text().strip()
            # Filter out boilerplate, short copyright strings, or social links
            if len(text) > 40 and not re.search(r'(?i)cookie|subscribe|all rights reserved|terms of service', text):
                paragraphs.append(text)

    body_text = "\n\n".join(paragraphs)

    if not body_text and target_container:
        body_text = target_container.get_text(separator=" ", strip=True)
        # Collapse multiple spaces
        body_text = re.sub(r'\s{2,}', ' ', body_text)

    if len(body_text) < 60:
        return {
            "success": False,
            "error": "Extracted text is too short or blocked by paywall/anti-scraping bot protection.",
            "domain": domain,
            "url": url,
            "title": title
        }

    return {
        "success": True,
        "url": url,
        "domain": domain,
        "title": title if title else "Untitled Article",
        "author": author,
        "publish_date": publish_date,
        "body_text": body_text[:12000]  # Cap length for analysis
    }
