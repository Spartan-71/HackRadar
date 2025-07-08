import requests
from datetime import datetime
from backend.models import Hackathon
from pydantic import ValidationError

def parse_hackathon_dates(date_str: str):
    """
    Parses date strings from Devpost API like:
    - 'May 26 - Jul 10, 2025' (different months)
    - 'Jul 10 - 20, 2025' (same month)
    - 'Jul 10, 2025' (single day)
    """
    if not date_str or not isinstance(date_str, str):
        return None, None

    try:
        if ' - ' in date_str:
            start_str, end_str = date_str.split(' - ')
            
            year = end_str.split(',')[-1].strip()
            
            month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            has_month = any(month in end_str for month in month_names)

            if has_month:
                full_start_str = f"{start_str}, {year}"
                full_end_str = end_str
            else:
                month = start_str.split(' ')[0]
                full_start_str = f"{start_str}, {year}"
                full_end_str = f"{month} {end_str}"

            start_date = datetime.strptime(full_start_str, "%b %d, %Y").date()
            end_date = datetime.strptime(full_end_str, "%b %d, %Y").date()
            return start_date, end_date
        else:
            date = datetime.strptime(date_str, "%b %d, %Y").date()
            return date, date
    except (ValueError, IndexError):
        return None, None

def fetch_devpost_hackathon() -> list[Hackathon]:
    """
    Fetches and validates hackathon data from the official Devpost API.
    """
    url = "https://devpost.com/api/hackathons"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        hackathon_data = resp.json().get("hackathons", [])
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except ValueError:
        print("Error decoding JSON from response.")
        return []

    hackathons = []
    for item in hackathon_data:
        start_date, end_date = parse_hackathon_dates(
            item.get("submission_period_dates")
        )

        location = "Online"
        if item.get("displayed_location"):
            location = item["displayed_location"].get("location", "Online")

        try:
            hackathon = Hackathon(
                id=str(item.get("id")),
                title=item.get("title"),
                start_data=start_date,
                end_date=end_date,
                location=location,
                url=item.get("url"),
                source="devpost",
                tags=[theme["name"] for theme in item.get("themes", [])]
            )
            hackathons.append(hackathon)
        except ValidationError as e:
            print(f"Skipping hackathon due to validation error: {item.get('title')}")
            print(e)
    
    return hackathons


