import threading
import time
from multiprocessing import Process

class Scheduler:

    def __init__(self):
        self.jobs = []
        self.dt = [] # seconds

    def periodic(self):
        t0 = [time.perf_counter_ns() for i in range(len(self.jobs))]
        while True:
            # print("2 here")
            t = time.perf_counter_ns()

            for i in range(len(self.jobs)):
                if (t - t0[i] > self.dt[i] * 10 ** 9):
                    try:
                        self.jobs[i]()
                    except Exception as e:
                        print(e)
                    t0[i] = t
            time.sleep(0.01)

    def start(self):
        # reader_thread = threading.Thread(target=self.periodic, daemon=True)
        # reader_thread.start()

        p = Process(target=self.periodic)
        p.start()

        return
    
    def add_job(self, job, freq):
        self.jobs.append(job)
        self.dt.append(1.0 / freq)
