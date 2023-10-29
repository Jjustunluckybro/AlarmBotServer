from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.services.jobs.alarm_status_check_job import check_queue_status


def create_and_start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_queue_status, "interval", seconds=60)
    scheduler.start()
    return scheduler
