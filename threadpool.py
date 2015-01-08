#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple ThreadPool library.


"""

from Queue import Queue
from threading import Event, Thread

class ThreadPool(object):
    def __init__(self, max_thread=10):
        self.max_thread = max_thread
        self.task_queue = Queue()
        self.threads = []

        for i in xrange(self.max_thread):
            self.threads.append(Worker(self.task_queue))    
        self.started = True

    def add_task(self, func, *args, **kwargs):
        """Add a task to task_queue"""
        if not self.started:
            return False
        else:
            self.task_queue.put((func, args, kwargs))
            return True

    def stop(self):
        """Stop serve, return until all waiting tasks done"""
        if not self.started:
            return None
            
        self.started = False
        self.task_queue.join()
        
        # set exit flag
        for item in self.threads:
            item.exit()
        # unblock all thread
        for item in self.threads:
            self.task_queue.put((None, (), {}))
        # wait all thread exit
        for item in self.threads:
            item.join()
        
        self.threads = []
        self.task_queue.join()
        
        
class Worker(Thread):
    def __init__(self, task_queue):
        self.__task_queue = task_queue
        self.__stop = Event()
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    def exit(self):
        self.__stop.set()
        
    def run(self):
        while True:
            func, args, kwargs = self.__task_queue.get(True)

            try:
                if self.__stop.is_set():
                    break
                func(*args, **kwargs)
            except Exception, e: 
                print func.__name__, ':', e
            finally:
                self.__task_queue.task_done()  

            
if __name__ == '__main__':
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
