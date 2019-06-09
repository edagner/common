import logging
import time
import threading
from queue import Queue
from work_config import *

logging.config.dictConfig(log_dict)
log = logging.getLogger("thread")
logging = logging.getLogger("general")


class Job:
    def __init__(self, value):
        self.value = value[0]
        self.job_order = value[1][0]
        self.jobs_finished = value[1][1]
        self.to_do = [x for x in self.job_order if x not in self.jobs_finished]
        self.applied_job_order = list()
        self.current_job = self.to_do.pop(0) if len(self.to_do) > 0 else None
        self.done = False

    def finish_job(self):
        finished_job = self.current_job
        self.current_job = self.to_do.pop(0) if len(self.to_do) > 0 else None
        log.debug("{} just finished task {}. On to {}".format(self.value, finished_job, self.current_job))

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
        log.debug("Working on job: {}".format(job.value))
        job.applied_job_order.append(1)
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
        log.debug("Working on job: {}".format(job.value))
        job.applied_job_order.append(2)
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
        log.debug("Working on job: {}".format(job.value))
        job.applied_job_order.append(3)
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
        log.debug("Working on job: {}".format(job.value))
        job.applied_job_order.append(4)
        job.finish_job()
        sort_q.put(job)


def sorter(multi_q, add_q, div_q, minus_q, sort_q, finished_list, job_num):
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
            finished_list.append(job)
            if len(finished_list) == job_num:
                tkill = "Poison"
                multi_q.put(tkill)
                add_q.put(tkill)
                div_q.put(tkill)
                minus_q.put(tkill)
                sort_q.put(tkill)


if __name__ == "__main__":
    work_list = generate_work()

    multi_queue = Queue(10)
    add_queue = Queue(10)
    div_queue = Queue(10)
    minus_queue = Queue(10)
    sorter_queue = Queue(10)

    finished_job_list = list()

    logging.debug(work_list)

    # current_jobs = list()
    # job_limit = 3

    # while len(work_list) != 0:
    #     current_jobs.append(work_list.pop(0))
    #     if len(current_jobs) =120= 3:
    #         for i in range(2):

    sort_thread = threading.Thread(
        target=sorter,
        args=(multi_queue, add_queue, div_queue, minus_queue, sorter_queue, finished_job_list, len(work_list))
        )
    sort_thread.start()

    for name, work in work_list.items():
        unit = (name, work)
        logging.debug(unit)
        job = Job(unit)
        sorter_queue.put(job)

    thread_list = list()

    for i in range(2):
        multi_thread = threading.Thread(target=multi, args=(multi_queue, sorter_queue,))
        add_thread = threading.Thread(target=add, args=(add_queue, sorter_queue,))
        div_thread = threading.Thread(target=div, args=(div_queue, sorter_queue,))
        minus_thread = threading.Thread(target=minus, args=(minus_queue, sorter_queue,))

        thread_list.append(multi_thread)
        thread_list.append(add_thread)
        thread_list.append(div_thread)
        thread_list.append(minus_thread)

        multi_thread.start()
        add_thread.start()
        div_thread.start()
        minus_thread.start()

    for t in thread_list:
        t.join()

    sort_thread.join()

    i = 1