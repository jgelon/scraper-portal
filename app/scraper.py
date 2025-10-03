import re
from bs4 import BeautifulSoup
from registry import SCRAPER_REGISTRY, scrape_content
from database import get_all_entries, update_last_values
from emailer import send_email
from playwright.sync_api import sync_playwright

def get_scraper_for_url(url):
    for pattern, func in SCRAPER_REGISTRY.items():
        if re.search(pattern, url):
            return func
    return scrape_content  # default

def scrape_dynamic(url, selectors):
    scraper = get_scraper_for_url(url)
    return scraper(url, selectors)

def scrape_content_playwright(url, selectors):
    try:      
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector(selectors[0])  # wait for content to load
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            print(soup.select_one("div.my-css-selector").text)
            return [soup.select_one(sel).get_text(strip=True) if soup.select_one(sel) else None for sel in selectors]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [None, None, None]
    
def check_all_entries():
    entries = get_all_entries()
    for entry in entries:
        entry_id, url, sel1, sel2, sel3, last1, last2, last3 = entry
        selectors = [sel1, sel2, sel3]
        new_values = scrape_dynamic(url, selectors)

        changes = []
        if new_values[0] != last1:
            changes.append(f"Selector 1 changed: '{last1}' → '{new_values[0]}'")
        if new_values[1] != last2:
            changes.append(f"Selector 2 changed: '{last2}' → '{new_values[1]}'")
        if new_values[2] != last3:
            changes.append(f"Selector 3 changed: '{last3}' → '{new_values[2]}'")

        if changes:
            message = f"Changes detected for {url}:\n" + "\n".join(changes)
            send_email("Webscraper Alert", message)

        update_last_values(entry_id, *new_values)

# scrape_content("https://www.hollandandbarrett.nl/shop/product/natures-aid-vitamine-d3-drops-baby-s-kids-60017597", ["div[class*='AddToBasket'][class*='prices']"])

