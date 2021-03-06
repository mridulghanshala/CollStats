import Helper
import threading
import json
DB = json.load(open("db.json"))
ALL = []
THREADS = []
SEARCH_COUNT = {}
KEYWORDS = ["fall", "spring", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

def search_all(thread,filter_by=None):
    THREADS.append(thread)
    if THREADS[-1] not in SEARCH_COUNT:
        SEARCH_COUNT[THREADS[-1]] = 0
    Search(thread)
    database_get = json.load(open("db.json"))[thread.partition(".com/")[2].partition("/")[0]]
    if filter_by!=None:
        if filter_by.lower()=="freshman":
            for v in database_get.keys():
                toRemove = []
                for val in database_get[v]:
                    if 'transfer' in str(val).lower():
                        toRemove.append(val)
                for val in toRemove:
                    database_get[v].remove(val)
        else:
            for v in database_get.keys():
                toRemove = []
                for val in database_get[v]:
                    if filter_by.lower() not in str(val).lower():
                        toRemove.append(val)
                for val in toRemove:
                    database_get[v].remove(val)
    return database_get, SEARCH_COUNT[thread]


class Search(object):
    def __init__(self, urlVal):
        self.main_url = urlVal
        self.thread_name = urlVal.partition(".com/")[2].partition("/")[0]
        if self.thread_name not in DB:
            DB[self.thread_name] = {'accepted': [], 'rejected': [], 'unknown': []}
            self.pages = Helper.get_page_count(self.main_url)
            print(self.pages)
            self.all_threads = []
            threads=list()
            for i in range(1, self.pages+1):
                for v in Helper.get_all_uni_threads(self.main_url + "//p{}".format(i)):
                    self.all_threads.append(v)
            for ar in self.all_threads:
                x = threading.Thread(target=Helper.extract_from_thread_url, args=(self.thread_name, ar,))
                threads.append(x)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            for val in ALL:
                print(val)
            with open('db.json', 'w') as outfile:
                json.dump(DB, outfile, indent=4)


