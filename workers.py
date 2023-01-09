import requests
from queue import Queue, Empty
from threading import Thread
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor

class Worker(Thread):
    def __init__(self, queue: Queue, output: list, *args, **kwargs):
        self.queue = queue
        self.output = output
        super().__init__(*args, **kwargs)
        
        self.daemon = True
        
        self.session = requests.session()        
        
    def run(self):
        while True:
            try:
                work = self.queue.get(timeout=10)  # 3s timeout
            except Empty:
                return
            
            # do whatever work you have to do on work
            request = self.session.get(work['url'])
            result = work['function'](request.text)
            
            self.output.append(result)
            
            self.queue.task_done()
            

    
