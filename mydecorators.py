import os
import time
import logging
import datetime


def decoratorWithArgs(myArg):
    def wrapper(func):
        print(myArg)

        def func_wrapper(*arg, **kwarg):
            print(func.__name__ + "Started")

            response = func(*arg, **kwarg)

            print(func.__name__ + "Finished")
            return response
        return func_wrapper
    return wrapper


def normalDecorator(func):
    def wrapper():
        print("taking time")
        t1 = time.time()
        func()
        t2 = time.time()
        print("Time it took to run the function: " + str((t2 - t1)))
    return wrapper


@decoratorWithArgs("zoo")
def testMe(n1, n2):
    print("Test function")
    return (n1+n2)


@normalDecorator
def test2():
    print("Test 2")
    time.sleep(1)


if __name__ == '__main__':
    datetimestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    initializeLog(datetimestr)
    logging.debug("20")
    testMe(1, 2)
    test2()
