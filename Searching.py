import Helper
import json


DB = json.load(open("db.json"))
def search_all(thread,filter_by=None):
    Search(thread)


class Search(object):
    def __init__(self, urlVal):
        self.main_url = urlVal
        self.thread = urlVal.partition(".com/")[2].partition("/")[0]
        DB[self.thread] = {'accepted': [], 'rejected': [], 'unknown': []}
        self.pages = Helper.get_page_count(self.main_url)
        print(self.pages)

