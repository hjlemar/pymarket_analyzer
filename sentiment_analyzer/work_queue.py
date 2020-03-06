import queue
import threading

from sentiment_analyzer.sentiment import determine_store_sentiment

q = queue.Queue()
threads = []

class WorkQueue:

  def __init__(self, callable, nthreads=3):
    self.callable = callable
    self.nthreads = nthreads
    self.threads = []
    self.q = queue.Queue()

  def run(self):    
    for i in range(self.nthreads):
      t = threading.Thread(target=self.process)
      t.start()
      self.threads.append(t)

          
  def enqueue(self,item):
    self.q.put(item)
    print("Submitted task")

  
  def process(self):
    while True:
      item = self.q.get()
      if item is not None:
        try:
          # process
          self.callable(item)
        except Exception as ex:
          ex.with_traceback()
          print("Error while processing item {}".format(item))
        finally:
          self.q.task_done()


sentiment_wq = WorkQueue(callable=determine_store_sentiment, threads=3)
sentiment_wq.run()

# global_wq = WorkQueue(callable=global_worker, threads=3)
# global_wq.run()