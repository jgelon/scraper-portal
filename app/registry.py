from bs4 import BeautifulSoup
import requests


SCRAPER_REGISTRY = {}

def register_scraper(domain_pattern):
    def decorator(func):
        SCRAPER_REGISTRY[domain_pattern] = func
        return func
    return decorator

#################### SCRAPERS ####################

# Default scraper using requests and BeautifulSoup
def scrape_content(url, selectors):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [soup.select_one(sel).get_text(strip=True) if soup.select_one(sel) else None for sel in selectors]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [None, None, None]


@register_scraper(r"hollandandbarrett\\.nl")
def scrape_hollandandbarrett(url, selectors):
    # custom scraping logic for this site
    ...
