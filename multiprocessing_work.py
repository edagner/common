import multiprocessing
import queue
import time
import os
import logging


def split_work():
    manager = multiprocessing.Manager()
    work_queue = manager.Queue(50)
    res_queue = manager.Queue(100)

    work_proc = multiprocessing.Process(target=generate_work_units, args=(work_queue, ))
    work_proc.start()

    # for cpu in range(4):
    #     multi_work = multiprocessing.Process(target=multiply, args=(work_queue, ))
    #     multi_work.start()

    # for cpu in range(4):
    #     multi_work.join()

    multi_count = 4
    multi_pool = multiprocessing.Pool(processes=multi_count)
    multi_list = list()
    res_list = list()
    for i in range(multi_count):
        multi_res = multi_pool.apply_async(multiply, (work_queue, res_queue, ))
        multi_list.append(multi_res)

    add_count = 2
    add_pool = multiprocessing.Pool(processes=add_count)
    for i in range(add_count):
        add_res = add_pool.apply_async(add_stuff, (res_queue, ))
        res_list.append(add_res)

    multi_pool.close()
    multi_pool.join()

    res_queue.put("Poison")

    add_pool.close()
    add_pool.join()
    work_proc.join()

    for m_res in multi_res:
        m_res.get()
    for a_res in add_res:
        a_res.get()


def add_stuff(res_q):
    while res_q.qsize() == 0:
        time.sleep(.1)
        print("add waiting")
    time.sleep(.1)
    while True:
        res = res_q.get()
        if res == "Poison":
            res_q.put(res)
            break
        new_res = res + 2
        print(new_res, os.getpid())


def multiply(work_q, res_q):
    while work_q.qsize() == 0:
        time.sleep(1)
    time.sleep(.1)
    while True:
        work = work_q.get()
        if work == "Poison":
            work_q.put(work)
            break
        res = work[0] * work[1]
        print(res, os.getpid())
        res_q.put(res)


def generate_work_units(work_queue):
    for i in range(1000):
        min = i * 500
        max = (i + 1) * 500
        work_unit = [min, max, i]
        work_queue.put(work_unit)
    work_queue.put("Poison")

if __name__ == "__main__":
    split_work()
