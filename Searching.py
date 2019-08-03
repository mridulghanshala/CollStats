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

def search_all(thread,filter_by=None):
    Search(thread)

class Search(object):
    def __init__(self, urlVal):
        self.main_url = urlVal
        self.thread_name = urlVal.partition(".com/")[2].partition("/")[0]
        DB[self.thread_name] = {'accepted': [], 'rejected': [], 'unknown': []}
        self.pages = Helper.get_page_count(self.main_url)
        print(self.pages)
        self.all_threads = []
        for i in range(1, self.pages+1):
            for v in Helper.get_yearly_threads(self.main_url + "//p{}".format(i)):
                self.all_threads.append(v)
                Helper.extract_from_thread_url(self.thread_name,self.all_threads[0])
       # threads = [threading.Thread(target=Helper.extract_from_thread_url, args=(self.thread, ar,)) for ar in self.all_threads]


