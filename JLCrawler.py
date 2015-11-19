# coding:utf-8
from JLModel import News
from bs4 import BeautifulSoup
import urllib.request
import time
import re


class Crawler():

    """the Crawler"""

    # def __init__(self, initial_url, que):
    # super(Crawer, self).__init__()
    #     self.initial_url = initial_url
    #     self.que = que
    #     self.que.put(initial_url)

    def __init__(self, que, visited, news, rlock):
        # super(Crawer, self).__init__()
        # self.initial_url = initial_url
        self.que = que
        self.visited = visited
        self.rlock = rlock
        self.news = news
        # self.que.put(initial_url)

    def get_re_string(self):
        date_string = time.strftime("/%y/%m%d/")
        re_string = 'http://news.163.com' + date_string + '\d{2}/\w{16}.html'
        # print(re_string)
        return re_string

    def is_crawl_url(self, url):
        if url is None:
            return False
        # elif 'http://news.163.com/15' not in url:
        #     return False
        return url.startswith('http://news.163.com/')

    # def news_handle(self, url):
    #     try:
    #         html = urllib.request.urlopen(url).read().decode('gbk')
    #         if html:
    #             news = News(html)
    #             self.que.put(url)
    #     except:
    #         print('err:' + url)

    def is_news_url(self, url):
        # global g_news
        # match = re.match(
            # r'http://news.163.com/\d{2}/\d{4}/\d{2}/\w{16}.html', url)
        p = re.compile(self.get_re_string())
        match = p.match(url)
        if match:
            news_url = match.group(0)
            return news_url
        else:
            return False

    def crawl(self):
        # time = 20
        url = self.que.get()
        if url not in self.visited:
            if self.rlock.acquire():
                self.visited.add(url)
                self.rlock.release()
        else:
            return

        try:
            # html = urllib.request.urlopen(url).read().decode('gbk')
            req = urllib.request.Request(url, headers={
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            })
            html = urllib.request.urlopen(req, timeout=30).read().decode('gbk')
            if html:
                soup = BeautifulSoup(html, 'lxml')
                if self.is_news_url(url):
                    # print(self.news)
                    print(url)
                    if url not in self.news:
                        news = News(soup, url)
                        lenth = len(news.content)
                        if lenth > 0:
                            try:
                                news.add()
                                if self.rlock.acquire():
                                    self.news.add(url)
                                    self.rlock.release()
                            except Exception as e:
                                raise e
                    else:
                        print(url + ' is exist')
                links = soup.find_all('a')
                for link in links:
                    # get url in link
                    link_url = link.get('href')
                    if self.is_crawl_url(link_url):
                        # print(link_url)
                        # insert into the queue
                        # self.is_news_url(link_url)
                        if not self.is_news_url(link_url):
                            self.que.put(link_url)
                        else:
                            self.que.put(self.is_news_url(link_url))
        except Exception as e:
            if self.is_news_url(url):
                print('err:' + url)
                print('exception:' + str(e))
