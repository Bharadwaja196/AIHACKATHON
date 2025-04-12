import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from cloud_trainer import perform_night_training  # Assuming cloud_trainer.py has this function
from night_trainer import fine_tune_model  # Assuming night_trainer.py has this function

# Set up logging to track scheduler events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job_listener(event):
    """
    Listener to log job execution results (success or failure).
    """
    if event.exception:
        logger.error(f"Job {event.job_id} failed.")
    else:
        logger.info(f"Job {event.job_id} executed successfully.")

def scheduled_task():
    """
    Function that is scheduled to run at night
    This will invoke nightly training and any other periodic tasks.
    """
    logger.info("Starting nightly training...")

    try:
        # Trigger the cloud trainer to do the fine-tuning job
        perform_night_training()
        # Optionally, trigger the fine-tuning from night_trainer
        fine_tune_model()

        logger.info("Nightly training and fine-tuning completed successfully.")
    except Exception as e:
        logger.error(f"Error during nightly training: {e}")

def start_scheduler():
    """
    Start the scheduler that runs the scheduled task
    """
    scheduler = BlockingScheduler()

    # Add listener for job events (execution success or failure)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Schedule the task to run every night at midnight (00:00)
    scheduler.add_job(scheduled_task, 'cron', hour=0, minute=0, id="nightly_training_job")

    logger.info("Scheduler started. Waiting for the next task.")
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
