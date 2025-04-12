import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from cloud_trainer import CloudTrainer  # Updated to use the class
from night_trainer import fine_tune_model  # Assume this accepts user_id + data

# Setup basic logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Dummy list of users – in real app, fetch from DB or user_manager.py
user_ids = ["user1", "user2"]

def job_listener(event):
    """
    Listener to log job execution results (success or failure).
    """
    if event.exception:
        logger.error(f"❌ Job {event.job_id} failed.")
    else:
        logger.info(f"✅ Job {event.job_id} executed successfully.")

def scheduled_task():
    """
    Function that runs at scheduled time, triggers nightly training and fine-tuning.
    """
    logger.info("🌙 Starting nightly training session for all users...")

    for user_id in user_ids:
        try:
            trainer = CloudTrainer(user_id)
            training_data = trainer.fetch_training_data()
            embeddings = trainer.fetch_embeddings()

            if not training_data:
                logger.warning(f"⚠️ No training data found for user {user_id}, skipping...")
                continue

            logger.info(f"🚀 Running fine-tuning for user {user_id} with {len(training_data)} items.")
            fine_tune_model(user_id=user_id, data=training_data, embeddings=embeddings)

            logger.info(f"🎉 Training complete for user {user_id}.")

        except Exception as e:
            logger.error(f"🔥 Error training user {user_id}: {e}")

def start_scheduler():
    """
    Start the APScheduler to run the nightly training task at midnight.
    """
    scheduler = BlockingScheduler()

    # Log job completion/failure
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Schedule the training task daily at midnight
    scheduler.add_job(
        scheduled_task,
        trigger='cron',
        hour=0,
        minute=0,
        id="nightly_training_job"
    )

    logger.info("⏰ Nightly training scheduler started. Waiting for 00:00...")
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
