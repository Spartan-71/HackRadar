from apscheduler.schedulers.background import BackgroundScheduler
from tasks.fetch_and_store import run
import logging

scheduler = BackgroundScheduler()

def start_scheduler():
    logging.info("Starting scheduler...")
    scheduler.add_job(run, 'interval', hours=12)
    logging.info("Scheduled 'run' job to execute every 12 hours.")
    scheduler.start()
    logging.info("Scheduler started.")
