import requests
from backend.schemas import Hackathon
from datetime import datetime

def fetch_dorahacks_hackathons() -> list[Hackathon]:
    base_url = "https://dorahacks.io/api/hackathon/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        all_hackathons = []
        # Fetch upcoming and ongoing hackathons with pagination
        for status in ["upcoming", "ongoing"]:
            url = base_url
            params = {"page": 1, "page_size": 24, "status": status}
            
            while url:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                all_hackathons.extend(data.get('results', []))
                
                # Get the next page URL, if it exists
                url = data.get('next')
                # Subsequent requests use the full URL from 'next', so we clear params
                params = None
        
        hackathons_data = []
        for hack in all_hackathons:
            start_date = datetime.fromtimestamp(hack.get("start_time")) if hack.get("start_time") else None
            end_date = datetime.fromtimestamp(hack.get("end_time")) if hack.get("end_time") else None
            
            hackathon = Hackathon(
                id=str(hack.get('id')),
                title=hack.get("title"),
                url=f"https://dorahacks.io/hackathon/{hack.get('uname')}/detail",
                start_date=start_date.date() if start_date else None,
                end_date=end_date.date() if end_date else None,
                location=hack.get("participation_form"),
                source="dorahacks"
            )
            hackathons_data.append(hackathon)

        return hackathons_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hackathons from DoraHacks: {e}") 
        return []