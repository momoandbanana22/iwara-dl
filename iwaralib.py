import os
os.path.join(os.path.dirname(__file__))
import re

from bs4 import BeautifulSoup

TRUE_VALUE = 0
FALSE_VALUE=-1

def encode(url):
    import urllib.parse
    print(urllib.parse.quote(url))

def login_key(html):
    fullpage = BeautifulSoup(html, "html.parser")
    h = fullpage.find("head")
    capture = h.find("script", text=re.compile("antibot")).string.strip()
    start = capture.find("\"key\":") + 7 # "key":"
    end   = capture.find("\"", start)
    print (capture[start:end])

def parse_title(html):
    fullpage = BeautifulSoup(html, "html.parser")
    try:
        print(fullpage.find("h1", class_="title").string[:75])
    except:
        exit(1)

def is_private(html):
    fullpage = BeautifulSoup(html, "html.parser")
    for h1 in fullpage.find_all("h1"):
        if "Private video" == h1.string:
            exit(TRUE_VALUE)
    exit(FALSE_VALUE)

dl_keyword_list = ["download", "drive.google.com", "mega", "mediafire.com", "dl", "1080p", "60fps", "bowlroll"]
def grep_keywords(html):
    try:
        fullpage = BeautifulSoup(html, "html.parser")
        paragraphs = fullpage.find("div", class_="node-info").find_all("p")

        buf = str()
        have_special_kw = False
        have_link = False
        for paragraph in paragraphs:
            v = str(paragraph).lower()
            for kw in dl_keyword_list:
                if kw in v:
                    have_special_kw = True
                    break
            if paragraph.find("a") != None:
                have_link = True
            buf += paragraph.prettify()

        if have_special_kw and have_link:
            print ("------------ Found better version in description ------------")
            print (buf)
            print ("-------------------------------------------------------------")
    except: pass


def is_youtube(html):
    fullpage = BeautifulSoup(html, "html.parser")
    for ytdl in fullpage.find_all("iframe"):
        if "youtu" in ytdl.get("src"):
            print(ytdl.get("src"))
            exit(TRUE_VALUE)
    exit(FALSE_VALUE)

def find_videoid(html):
    fullpage = BeautifulSoup(html, "html.parser")
    a_tags = fullpage.find_all("a");

    urls = set()
    for tag in a_tags:
        if "/videos/" in tag.get("href"):
            urls.add(tag.get("href").split("/")[-1].split("?")[0])

    for url in urls:
        print (url, end="`")

def find_userid(html):
    fullpage = BeautifulSoup(html, "html.parser")
    a_tags = fullpage.find_all("a");

    users = set()
    for tag in a_tags:
        if not (tag.get("href") is None):
            if "/users/" in tag.get("href"):
                print ( tag.get("href").split("/")[-1].split("?")[0] , end="`")
                exit

def find_max_user_video_page(html):
    fullpage = BeautifulSoup(html, "html.parser")
    try:
        print(fullpage.find("li", class_="pager-last").find("a").get("href").split("=")[-1])
    except:
        print(0)


# iwara-friend functions
def find_pending_user_list(html):
    fullpage = BeautifulSoup(html, "html.parser")
    ids = set()
    for btn in fullpage.find_all("button", class_="accept-friend"):
        ids.add(btn.get("data-frid"))

    for idv in ids:
        print (idv, end="`")
