import multiprocessing
import time


def multipy(work_queue):
    try:
        for i in range(10):
            res = i*2
            print res, "multipy"
            work_queue.put(res)
        work_queue.put("PoisonPill")
    except Exception as e:
        print e

def add(work_queue, result_list):
    try:
        while True:
            while work_queue.qsize() == 0:
                time.sleep(.01)

            num = work_queue.get()

            if num == "PoisonPill":
                break

            res = num + 5
            print res, "add"
            result_list.append(res)
    except Exception as e:
        print e


if __name__=="__main__":

    manager = multiprocessing.Manager()
    work_pool=multiprocessing.Pool(4)

    work_q = manager.Queue(5)
    res_list = manager.list()

    async_res = []

    async_res.append(work_pool.apply_async(multipy, (work_q,)))
    
    async_res.append(work_pool.apply_async(add, (work_q, res_list,)))

    work_pool.close()
    work_pool.join()

    print res_list
    for res in async_res:
        res.get()
