
import multiprocessing
import time
import mylogging
import logging



def multiply(m_queue, a_queue):
    try:
        print multiprocessing.current_process()
        while True:
            if m_queue.qsize() == 0:
                continue
            num = m_queue.get()

            if num == "PoisonPill":
                a_queue.put("PoisonPill")
                break

            res = num * 2
            print res, "multipy"
            a_queue.put(res)
    except Exception as e:
        print e

def add(work_queue, result_list):
    try:
        print multiprocessing.current_process()
        while True:
            if work_queue.qsize() == 0:
               continue

            num = work_queue.get()

            if num == "PoisonPill":
                break

            res = num + 5
            print res, "add"
            result_list.append(res)
    except Exception as e:
        print e

def foo():
    logging.debug("lark")

if __name__ == "__main__":
    mylogging.initializeLog()

    logging = logging.getLogger('queue_log')

    manager = multiprocessing.Manager()
    work_pool = multiprocessing.Pool(8)

    print "Number of cores: {}".format(multiprocessing.cpu_count())

    multi_q = manager.Queue(1000)
    add_q = manager.Queue(1000)
    res_list = manager.list()

    async_res = []

    for i in range(80):
        multi_q.put(i)

    multi_q.put("PoisonPill")

    async_res.append(work_pool.apply_async(multiply, (multi_q, add_q,)))
    
    async_res.append(work_pool.apply_async(add, (add_q, res_list,)))

    work_pool.close()
    work_pool.join()

    foo()
    logging.info(res_list)
    for res in async_res:
        res.get()