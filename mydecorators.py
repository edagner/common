import os
import time

def decoratorWithArgs(moo):
    def wrapper(func):
        print moo
        def func_wrapper(*arg, **kwarg):
            print "do this"

            func(*arg, **kwarg)

            print "I finished this"
        return func_wrapper
    return wrapper

def normalDecorator(func):
    def wrapper():
        print "taking time"
        t1 = time.time()
        func()
        t2 = time.time()
        return "Time it took to run the function: " + str((t2 - t1))
    return wrapper

@decoratorWithArgs("zoo")
def test():
    print "Test function"

@normalDecorator
def test2():
    print "Test 2"
    time.sleep(2)

def main():
    test()
    test2()

if __name__ == '__main__':
    main()