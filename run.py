# coding:utf-8
from JLQueue import JLQueue
from JLThread import ThreadPool
from JLModel import News
from JLModel import app

g_news = News.get_all_news()
g_queue = JLQueue()
g_visited = set()
# g_news = set()
g_threads = []
inital_url = 'http://news.163.com/'

g_queue.put(inital_url)
g_threadpool = ThreadPool(51, g_threads, g_queue, g_visited, g_news)
g_threadpool.start()
# run server
# JLServer.run()
app.run(host="127.0.0.1", port=25000)
g_threadpool.wait_for_complete()
# print(g_visited)
