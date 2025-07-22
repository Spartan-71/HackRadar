import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from adapters.devpost import fetch_devpost_hackathons
from adapters.unstop import fetch_unstop_hackathons
from adapters.dorahacks import fetch_dorahacks_hackathons
from adapters.mlh import scrape_mlh_events
from adapters.devfolio import scarpe_devfolio_hackathons

from backend.db import SessionLocal, Base, engine
from backend.crud import upsert_hackathon

Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def run():
    logging.info("Starting hackathon scraping run.")
    db = SessionLocal()
    logging.info("Database session opened.")
    sources = [
        ("MLH", scrape_mlh_events),
        ("Devpost", fetch_devpost_hackathons),
        ("Unstop", fetch_unstop_hackathons),
        ("DoraHacks", fetch_dorahacks_hackathons),
        ("Devfolio", scarpe_devfolio_hackathons),
    ]
    with ThreadPoolExecutor(max_workers=len(sources)) as executor:
        future_to_source = {executor.submit(fetch_func): name for name, fetch_func in sources}
        for future in as_completed(future_to_source):
            name = future_to_source[future]
            logging.info(f"Started fetching from {name}.")
            try:
                hackathons = future.result()
                logging.info(f"Fetched {len(hackathons)} hackathons from {name}.")
                for h in hackathons:
                    logging.debug(f"Upserting hackathon: {h}")
                    upsert_hackathon(db, h)
                logging.info(f"Completed upserting hackathons from {name}.")
            except Exception as e:
                logging.error(f"Error fetching from {name}: {e}")
    db.close()
    logging.info("Database session closed.")
    logging.info("Hackathon scraping run completed.")


if __name__ == "__main__":
    run()
