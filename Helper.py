import requests
import bs4
import lxml
import threading
import json
import Searching
def grabSite(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return requests.get(url, timeout=7, headers=headers)
    except Exception as exp:
        print (exp)
        pass
    return "<html></html>"

def subthread_url(url, num):
	return url.partition(".html")[0] + "-p{}.html".format(num)

def get_page_count(url):
    res = grabSite(url)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    try:
        return int(page.select(".LastPage")[0].getText())
    except:
        return 2

def get_yearly_threads(url):
    threads = []
    res = grabSite(url)
    page = bs4.BeautifulSoup(res.text, 'lxml')
    for wrapper in page.find_all('ul',class_="DataList Discussions"):
        for litag in wrapper.find_all('li'):
            x = litag.find('div', class_='Title')
            v=x.find(('a'))
            text=v.attrs['href']
            if 'talk.collegeconfidential.com' in text:
                threads.append(v['href'])
        return threads

def extract_from_thread_url(threadName, url):
    rCount = 0
    aCount = 0
    tempCount = get_page_count(url)
    for i in range(1, tempCount + 1):
        res = grabSite(subthread_url(url, i))
        page = bs4.BeautifulSoup(res.text, 'lxml')
        for thread in page.select(".Role_RegisteredUser"):
            comment = thread.select(".userContent")[0]
            username = str(thread).partition("/profile/")[2].partition('"')[0]
            if is_stats(str(comment.getText())):
                if 'accepted' in str(comment.getText()).lower():
                    typeVal = "accepted"
                # pass
                elif 'rejected' in str(comment.getText()).lower() or 'rejection' in str(comment.getText()).lower():
                    typeVal = "rejected"
                # pass
                else:
                    typeVal = "unknown"
                # pass
                Searching.DB[threadName][typeVal].append({'urls': [url], 'type': "direct", "comment": str(thread)})
            elif 'accepted' in str(comment.getText()).lower().split(" ")[:5] or 'rejected' in str(comment.getText()).lower().split(" ")[:5]:
                fullComment = get_stats_from_profile(username)

def is_stats(string):
    if 'gpa' in string.lower() and (string.count(":") > 2 or string.count("-") > 2):
        return True
    return False

def get_stats_from_profile(username):