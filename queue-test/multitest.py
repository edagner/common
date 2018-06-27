import multiprocessing


def multipy(x):
    res = x*2
    print res


if __name__=="__main__":
    work_pool=multiprocessing.Pool(4)

    async_res = []
    for i in range(4):
        async_res.append(work_pool.apply_async(multipy, (i,)))

    for res in async_res:
        res.get()
