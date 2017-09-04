import multiprocessing


def multiprocess(processNum, multiProcFunction, vars, taskList):
    try:
        pool = multiprocessing.Pool(processNum)
        for task in taskList: 
            asyncResult = pool.apply_async(multiProcFunction,(vars))
            poolResults.append(asyncResult)
        while poolResults:
            asyncResult = poolResults.pop()
            try:
                asyncResult.get(timeout=60)
            except multiprocessing.TimeoutError:
                poolResults.append(asyncResult)
        pool.close()
        pool.join()
        print asyncResult.successful()
        if not asyncResult.successful():
            raise Exception("Multiprocessing of {} Failed".
                format(multiProcFunction))
    except Exception as e:
        print e
        raise e