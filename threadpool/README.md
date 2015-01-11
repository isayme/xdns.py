threadpool.py
=============

A simple threadpool written in Python

How to use ?
============

    from threadpool import ThreadPool

    import time
    import random
    
    from threading import Lock
    
    lock = Lock()
    
    def test_func(ntime):
        time.sleep(ntime)
        lock.acquire()
        print('sleep {} seconds!'.format(ntime))
        lock.release()
    
    tp = ThreadPool()
    
    tasks = (random.randrange(1, 10) for i in xrange(5))
    
    for i in tasks:
        tp.add_task(test_func, i)
        
    tp.stop()

Contact
=======

email: isaymeorg@gmail.com
