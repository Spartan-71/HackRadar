from apscheduler.schedulers.background import BackgroundScheduler
from tasks.fetch_and_store import run


scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(run, 'interval', hours=12)
    scheduler.start()