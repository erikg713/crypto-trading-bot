from src.main import trading_job
from src.utils.scheduler import JobScheduler
from src.db.db_utils import init_db

if __name__ == "__main__":
    init_db()
    scheduler = JobScheduler()
    scheduler.add_job(trading_job, every=15, unit='minutes', job_name='Multi-Asset Trading Job')
    scheduler.run_forever()

