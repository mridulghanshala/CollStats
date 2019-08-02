import Helper
import json
import requests
import bs4
import lxml
import threading
import json
DB = json.load(open("db.json"))
ALL = []
KEYWORDS = ["fall", "spring", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

def get_yearly_threads(url):
    threads = []
    res = Helper.grabSite(url)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    for wrapper in page.find_all('ul',class_="DataList Discussions"):
        for litag in wrapper.find_all('li'):
            x = litag.find('div', class_='Title')
            v=x.find(('a'))
            text=v.attrs['href']
            if 'talk.collegeconfidential.com' in text:
                threads.append(v['href'])
                # print(v['href'])
        return threads


def search_all(thread,filter_by=None):
    Search(thread)

class Search(object):
    def __init__(self, urlVal):
        self.main_url = urlVal
        self.thread = urlVal.partition(".com/")[2].partition("/")[0]
        DB[self.thread] = {'accepted': [], 'rejected': [], 'unknown': []}
        self.pages = Helper.get_page_count(self.main_url)
        print(self.pages)
        self.all_threads = []
        for i in range(1, 10):
            for v in get_yearly_threads(self.main_url + "//p{}".format(i)):
                self.all_threads.append(v)
        for i in self.all_threads:
         print(i)


