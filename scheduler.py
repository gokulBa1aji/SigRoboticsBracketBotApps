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
                        start = time.perf_counter()
                        self.jobs[i]()
                        end = time.perf_counter()
                        elapsed = end - start
                        print(self.jobs[i].__name__, ": ")
                        print(f'Time taken: {elapsed:.6f} seconds')
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
