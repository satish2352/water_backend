from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import sub_update_scheduler

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(sub_update_scheduler, 'interval', minutes=5)
    scheduler.add_job(sub_update_scheduler, 'interval', hours=6 )
    scheduler.start()