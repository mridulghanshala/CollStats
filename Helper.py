import requests
import bs4
import lxml
import threading
import json
import Searching
import config
import time
def grabSite(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return requests.get(url, timeout=7, headers=headers)
    except Exception as exp:
        print (exp)
        pass
    return "<html></html>"

def grabSiteLogin(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        post_params = {
            "login": str(config.keys['login']),
            "pass": str(config.keys['pass']),
            "source":"database"
        }
        SAML={}
        with requests.Session() as s:
            getAuth=s.get(url,headers=headers)
            soup=bs4.BeautifulSoup(getAuth.content,'lxml')
            AuthState_dynamic = soup.find('input', attrs={'name': 'AuthState'})['value']
            myurl="https://auth.collegeconfidential.com/module.php/hobsonsregister/login.php?{}".format(AuthState_dynamic)
            post_params['AuthState']=str(AuthState_dynamic)
            post_login_form = s.post(myurl, data=post_params, headers=headers)
            parse_to_get_saml = bs4.BeautifulSoup(p.content,'lxml')
            samlcode = parse_to_get_saml.find('input', attrs={'name': 'SAMLResponse'})['value']
            SAML['SAMLResponse']=samlcode
            saml_post=s.post("https://talk.collegeconfidential.com/entry/connect/saml", data=SAML, headers=headers)
            page=s.get(url)
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
                else:
                    typeVal = "unknown"
                Searching.DB[threadName][typeVal].append({'urls': [url], 'type': "direct", "comment": str(thread)})
            # elif ('accepted' in str(comment.getText()).lower().split(" ")[:5] or 'rejected' in str(comment.getText()).lower().split(" ")[:5]):
            fullComment = get_stats_from_profile(username)
            print("here")

def is_stats(string):
    if 'gpa' in string.lower() and (string.count(":") > 2 or string.count("-") > 2):
        return True
    return False

def get_stats_from_profile(username):
    url="https://talk.collegeconfidential.com/profile/comments/{}".format(username)
    comments = []
    pages = None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        post_params = {
            "login": str(config.keys['login']),
            "pass": str(config.keys['pass']),
            "source":"database"
        }
        SAML={}
        with requests.Session() as s:
            getAuth=s.get(url,headers=headers)
            soup=bs4.BeautifulSoup(getAuth.content,'lxml')
            AuthState_dynamic = soup.find('input', attrs={'name': 'AuthState'})['value']
            myurl="https://auth.collegeconfidential.com/module.php/hobsonsregister/login.php?{}".format(AuthState_dynamic)
            post_params['AuthState']=str(AuthState_dynamic)
            post_login_form = s.post(myurl, data=post_params, headers=headers)
            parse_to_get_saml = bs4.BeautifulSoup(post_login_form.content,'lxml')
            samlcode = parse_to_get_saml.find('input', attrs={'name': 'SAMLResponse'})['value']
            SAML['SAMLResponse']=samlcode
            saml_post=s.post("https://talk.collegeconfidential.com/entry/connect/saml", data=SAML, headers=headers)
            all_comments=s.get(url)
            page = bs4.BeautifulSoup(all_comments.text, 'lxml')
    except Exception as exp:
        print (exp)
    if pages == None:
        # results = page.find_all('div', attrs={"class": "Profile-Stats"})
        for a in page.select('.Profile-Stats a'):
            if a['href']==("/profile/comments/"+username):
                nu=a.find('span',attrs={"class":"Count"})
                pages=int(nu.text)
                break
