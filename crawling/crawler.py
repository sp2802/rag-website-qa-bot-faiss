import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

SKIP = ["login", "signup", "cart", "register"]

def crawl_website(base_url, max_pages=30):
    visited, results = set(), []
    queue = deque([base_url])
    domain = urlparse(base_url).netloc

    while queue and len(results) < max_pages:
        url = queue.popleft()
        if url in visited or any(s in url.lower() for s in SKIP):
            continue
        visited.add(url)

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            results.append({
                "url": url,
                "title": soup.title.string if soup.title else "",
                "html": r.text
            })

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if urlparse(link).netloc == domain:
                    queue.append(link)
        except:
            pass

    return results