import threading
import queue
import time

from JLCrawler import Crawler


class MyThread(threading.Thread):

    """docstring for MyThread"""

    def __init__(self, que, visited, news, rlock):
        super().__init__()
        self.que = que
        self.visited = visited
        self.rlock = rlock
        self.news = news

    def run(self):
        while True:
            # print(str(self.que.get()) + str(self))
            # time.sleep(random.randint(5, 10))
            crawler = Crawler(self.que, self.visited, self.news, self.rlock)
            crawler.crawl()
            # print(str(self))
            # count -= count
            if self.que.empty():
                print('empty')
                break


class ThreadPool():

    """docstring for ThreadPool"""

    def __init__(self, num, threads, que, visited, news):
        self.num = num
        self.threads = threads
        self.que = que
        self.visited = visited
        self.rlock = threading.RLock()
        self.news = news

    def start(self):
        for i in range(self.num):
            thread = MyThread(self.que, self.visited, self.news, self.rlock)
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)

    def wait_for_complete(self):
        while len(self.threads):
            thread = self.threads.pop()
            print(len(self.threads))
            if thread.isAlive():
                thread.join()


# threads = []
# que = queue.Queue()
# tp = ThreadPool(5, threads, que)
# tp.strat()
# print(tp.threads)
# for i in range(10):
#     tp.add_job(i)
#     time.sleep(1)
# tp.wait_for_complete()
# print(threads)
