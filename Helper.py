import requests
import bs4
import lxml
import threading
import json

def grabSite(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return requests.get(url, timeout=7, headers=headers)
    except Exception as exp:
        print (exp)
        pass
    return "<html></html>"

def subthread_url(url, num):
	# https://talk.collegeconfidential.com/columbia-school-general-studies/2036962-dual-ba-program-trinity-college-dublin-and-columbia-university-fall-2018.html
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

