import bs4
import Helper
def parse_html(value):
    info = {}
    htmlString = value['comment']
    page = bs4.BeautifulSoup(htmlString, 'lxml')
    info['username'] = page.select(".Username")[0].getText()
    info['totalPosts'] = page.select("b")[0].getText()
    info['profilePic'] = str(page.select(".ProfilePhotoMedium")[0]).partition('src="')[2].partition('"')[0]
    info['dtString'] = str(page.select("time")[0]).partition('datetime="')[2].partition('"')[0].partition('T')[0]
    info['content'] = page.select(".userContent")[0]
    justification = ""
    if value['type'] == "direct":
        justification += """{} posted their stats <a href="{}">here</a>""".format(info['username'], value['urls'][0])
    else:
        justification = """{} posted their admission decision <a href="{}">here</a><br>""".format(info['username'],value['urls'][0])
        justification += """{} posted their stats <a href="{}">here</a>""".format(info['username'], value['urls'][1])
    info['justification'] = justification
    info['foundVia'] = value['type']
    info['url'] = value['urls'][0]
    info['title'] = ' '.join([x.title() for x in info['url'][::-1].partition('/')[0][::-1].partition('-')[2].replace(".html", "").split("-")])
    return info