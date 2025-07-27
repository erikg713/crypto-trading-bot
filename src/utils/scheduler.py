import schedule
import time
import threading
from typing import Callable, Union
import time
import threading

class JobScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, func, every=1, unit="seconds", job_name=None):
        self.jobs.append({"func": func, "interval": self._unit_to_seconds(every, unit), "name": job_name, "last_run": 0})

    def _unit_to_seconds(self, every, unit):
        units = {"seconds":1, "minutes":60, "hours":3600, "days":86400}
        return every * units.get(unit, 1)

    def run_forever(self):
        print("Scheduler started...")
        try:
            while True:
                now = time.time()
                for job in self.jobs:
                    if now - job["last_run"] >= job["interval"]:
                        print(f"Running job: {job['name']}")
                        threading.Thread(target=job["func"]).start()
                        job["last_run"] = now
                time.sleep(1)
        except KeyboardInterrupt:
            print("Scheduler stopped.")

class JobScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(
        self,
        job_func: Callable,
        every: Union[int, float] = 1,
        unit: str = "minutes",
        job_name: str = None
    ):
        """
        Add a job to the scheduler.

        :param job_func: Function to run.
        :param every: Interval (e.g., 1, 5, 0.5).
        :param unit: Unit of time. Options: "seconds", "minutes", "hours", "days".
        :param job_name: Optional name for logging.
        """
        job = schedule.every(every)
        job_method = getattr(job, unit)
        job_method.do(self._safe_wrapper(job_func, job_name))
        self.jobs.append(job)

    def _safe_wrapper(self, job_func: Callable, name: str = None):
        def wrapped():
            try:
                if name:
                    print(f"[⏰ Running job] {name}")
                job_func()
            except Exception as e:
                print(f"[⚠️ Job Error] {name or 'Unnamed'}: {e}")
        return wrapped

    def run_forever(self, interval: float = 1.0):
        """
        Run the scheduler in the current thread (blocking).
        """
        print("[🚀 Scheduler Started]")
        while True:
            schedule.run_pending()
            time.sleep(interval)

    def run_async(self, interval: float = 1.0):
        """
        Run the scheduler in a background thread.
        """
        thread = threading.Thread(target=self.run_forever, args=(interval,), daemon=True)
        thread.start()
        print("[🔁 Scheduler Running in Background]")
        return thread
