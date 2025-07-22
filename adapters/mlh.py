import cloudscraper
from bs4 import BeautifulSoup
from backend.schemas import Hackathon
import hashlib
from datetime import date

def scrape_mlh_events() -> list[Hackathon]:
    current_year = date.today().year + 1
    url = f"https://mlh.io/seasons/{current_year}/events"

    events = []
    scraper = cloudscraper.create_scraper()

    response = scraper.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch MLH page for season {current_year}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    event_divs = soup.find_all("div", class_="event")

    for event in event_divs:
        name_tag = event.find("h3", class_="event-name")
        name = name_tag.get_text(strip=True) if name_tag else ""

        link_tag = event.find("a", class_="event-link")
        link = link_tag.get('href', '') if link_tag else ""

        if not name or not link:
            continue

        date_tag = event.find("p", class_="event-date")
        date_str = date_tag.get_text(strip=True) if date_tag else ""

        start_date_tag = event.find("meta", itemprop="startDate")
        start_date = start_date_tag['content'] if start_date_tag else ""

        end_date_tag = event.find("meta", itemprop="endDate")
        end_date = end_date_tag['content'] if end_date_tag else ""


        location_tag = event.find("div", class_="event-location")
        city_tag = location_tag.find("span", itemprop="city") if location_tag else None
        city = city_tag.get_text(strip=True) if city_tag else ""

        state_tag = location_tag.find("span", itemprop="state") if location_tag else None
        state = state_tag.get_text(strip=True) if state_tag else ""

        format_tag = event.find("div", class_="event-hybrid-notes")
        format_type = format_tag.get_text(strip=True) if format_tag else "In-Person"
        
        location: str = "Online"
        if format_type=="In-Person Only":
            location=f"{city}, {state}"

        hackathon = Hackathon(
            id=hashlib.sha256(link.encode()).hexdigest(),
            title=name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            url=link,
            source="MLH"
        )

        events.append(hackathon)

    return events