from bs4 import BeautifulSoup

def extract_clean_text(page):
    soup = BeautifulSoup(page["html"], "html.parser")
    for tag in soup(["script","style","nav","footer","header","aside"]):
        tag.decompose()
    text = " ".join(soup.get_text().split())
    return {"url": page["url"], "title": page["title"], "text": text}