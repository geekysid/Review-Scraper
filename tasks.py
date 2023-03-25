# tasks.py
from celery import Celery
import time
from Modules import utils
import scraper


app = Celery("tasks", broker="redis://:@localhost:6379/0")
app.conf.result_backend = "redis://:@localhost:6379/1"
app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    result_expires=2592000,
)


TEST = 0


# >> FUNCTION TO RUN THE SCRAPER FOR A GIVEN JOB_ID
@app.task()
def run_scraper(job_id):
    scraper.main(job_id)


# >> FUNCTION TO COLLECT JOBS FROM DB AND ADDING TO QUEUE
def add_job_to_queue():
    # 1. get jobs that has status of ADDED
    job_ids = utils.get_new_jobs(max_count=4)
    print(f"Total {len(job_ids)} are to be added to queue")

    for job_id in job_ids:
        # 2. update status of all these jobs to QUEUED
        updated = utils.update_job_status(job_id, new_status='QUEUED', remarks="Added to Queue")
        # 3. add jobs to queue
        if updated:
            run_scraper.delay(job_id)
            print(f"  >> Job with ID {job_id} added to queue")
        else:
            print(f"  xx Unable to update the status of the job {job_id} so skipping.")


if __name__ == "__main__":
    add_job_to_queue()



# celery -A tasks worker --pool=solo --loglevel=INFO -n worker1@%h
# celery -A tasks worker --pool=solo --loglevel=INFO -n worker2@%h
# celery -A tasks worker --pool=solo --loglevel=INFO -n worker3@%h
