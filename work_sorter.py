import logging
import time
import threading
import queue
from work_config import *

logging.config.dictConfig(log_dict)
log = logging.getLogger("app")


class Job:
    def __init__(self, value):
        self.value = value[0]
        self.job_order = value[1][0]
        self.jobs_finished = value[1][1]
        self.to_do = [x for x in self.job_order if x not in self.jobs_finished]
        self.applied_job_order = list()
        self.current_job = self.to_do[0]
        self.done = False

    def finish_job(self):
        finished_job = self.to_do.pop(0) if len(self.to_do) > 0 else None
        log.debug("{} just finished task {}. On to {}".format(self.value, self.current_job, finished_job))
        self.current_job = finished_job

    def complete(self):
        self.done = True


def generate_work():
    work = {
        "a": [[4, 3, 2, 1], []],
        "b": [[1, 2, 3, 4], []],
        "c": [[2, 1, 3, 4], []],
        "d": [[1, 2, 4, 3], []],
        "e": [[1, 4, 3, 2], []],
        "f": [[1, 3, 4, 2], []]
    }

    return work


def multi(multi_q, sort_q):
    while True:
        if multi_q.qsize() == 0:
            time.sleep(1)
        job = multi_q.get()
        if job == "Poison":
            multi_q.put(job)
            break
        job.finished_job_order.append(1)
        job.finish_job()
        sort_q.put(job)


def add(add_q, sort_q):
    while True:
        if add_q.qsize() == 0:
            time.sleep(1)
        job = add_q.get()
        if job == "Poison":
            add_q.put(job)
            break
        job.finished_job_order.append(2)
        job.finish_job()
        sort_q.put(job)


def div(div_q, sort_q):
    while True:
        if div_q.qsize() == 0:
            time.sleep(1)
        job = div_q.get()
        if job == "Poison":
            div_q.put(job)
            break
        job.finished_job_order.append(3)
        job.finish_job()
        sort_q.put(job)


def minus(minus_q, sort_q):
    while True:
        if minus_q.qsize() == 0:
            time.sleep(1)
        job = minus_q.get()
        if job == "Poison":
            minus_q.put(job)
            break
        job.finished_job_order.append(4)
        job.finish_job()
        sort_q.put(job)


def sorter(multi_q, add_q, div_q, minus_q, sort_q):
    while True:
        if sort_q.qsize() == 0:
            time.sleep(1)
        job = sort_q.get()
        if job == "Poison":
            sort_q.put(job)
            break
        if job.current_job == 1:
            multi_q.put(job)
        elif job.current_job == 2:
            add_q.put(job)
        elif job.current_job == 3:
            div_q.put(job)
        elif job.current_job == 4:
            minus_q.put(job)
        else:
            job.complete()


if __name__ == "__main__":
    work = generate_work()
