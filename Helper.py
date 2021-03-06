import requests
import bs4
import Searching
import config

def grabSite(url):
    for i in range(3):
        Searching.SEARCH_COUNT[Searching.THREADS[-1]] += 1
        print(url)
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

def get_all_uni_threads(url):
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
            elif ('accepted' in str(comment.getText()).lower().split(" ")[:5] or 'rejected' in str(comment.getText()).lower().split(" ")[:5]):
                fullComment = get_stats_from_profile(username)
                temp = fullComment
                if temp != None:
                    temp = temp['comment'].getText()
                    if 'accepted' in str(temp).lower():
                        typeVal = "accepted"
                    elif 'rejected' in str(temp).lower() or 'rejection' in str(temp).lower():
                        typeVal = "rejected"
                    else:
                        typeVal = "unknown"
                    Searching.DB[threadName][typeVal].append({'urls': [url, str(fullComment['url'])], 'type': "profile","comment": str(fullComment['comment'])})
            rCount += str(comment).lower().count("rejected")
            aCount += str(comment).lower().count("accepted")
    x = {"url": url, "rCount": rCount, "aCount": aCount}
    Searching.ALL.append(x)
    return x

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
            while True:
                all_comments=s.get(url)
                page = bs4.BeautifulSoup(all_comments.text, 'lxml')
                if pages == None:
                    for a in page.select('.Profile-Stats a'):
                        if a['href'] == ("/profile/comments/" + username):
                            nu = a.find('span', attrs={"class": "Count"})
                            total_com = int(nu.text)
                            pages=range(2, len(range(0,total_com, 20)))
                            break
                for item in page.select(".Item"):
                    for val in item.select(".Message"):
                        if comment_in_profile(val.getText()):
                            comment_url = extract_complete_comment_url(item)
                            comment = get_specific_comment(comment_url)
                            if comment != None:
                                if is_stats(comment.getText()):
                                    return {'comment': comment, 'url': url}
                if len(pages) == 0:
                    return
                else:
                    url = "https://talk.collegeconfidential.com/profile/comments/{}?page=p{}".format(username,pages.pop(0))
    except Exception as exp:
        return None


def comment_in_profile(dig):
    s = dig.lower()
    return 'accepted' in s or 'rejected' in s or 'decision' in s or '!' in s

def extract_complete_comment_url(item):
    s= str(item).partition('a href="')[2].partition('"')[0]
    return s

def get_specific_comment(url):
    commentID = url.partition("#")[2]
    text=grabSite(url)
    page = bs4.BeautifulSoup(text.text, 'lxml')
    for val in page.select(".Role_RegisteredUser"):
        if val['id']==commentID:
            return val