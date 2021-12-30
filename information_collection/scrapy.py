import json
import requests


import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


DBLP_JOURNAL_PREVIX = "https://dblp.uni-trier.de/db/journals/"
SOURCE_DBLP_URL = "https://dblp.uni-trier.de/db/journals/index.html"
HEADER = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"}
JOURNAL_NUM_PER_PAGE = 100
JOURNAL_URLS_FILE = "./journal_urls.json"

DBLP_PREFIX = "dblp: "


def get_all_journal_names():
    urls = dict()
    start_num = 0
    while True:
        target = SOURCE_DBLP_URL + "?pos=" + str(start_num)
        req = requests.get(url=target, headers=HEADER)
        txt = req.text
        soup = BeautifulSoup(txt, features="lxml")
        
        if "no results" in soup.prettify():
            break

        body = soup.body
        # for child in soup.body.descendants:
        #     print(child)
        x = soup.find_all(id="browse-journals-output")
        y = x[0].find_all("div", class_="hide-body")
        z = y[0].find_all("a")
        for l_link in z:
            journal_name = l_link.string
            urls[journal_name] = l_link["href"]
        start_num = start_num + JOURNAL_NUM_PER_PAGE

    with open(JOURNAL_URLS_FILE, "w") as f:
        json.dump(urls, f)


def get_journal_urls_from_local_file():
    with open(JOURNAL_URLS_FILE, "r") as f:
        journal_urls = json.load(f)
    return journal_urls


def get_info_of_article(elsevier_url):
    req = requests.get(url=elsevier_url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    basic_info = json.loads(soup.body.script.string)

    # public  date
    print(basic_info["article"]["dates"])
    # title
    print(basic_info["article"]["title"]["content"][0]["_"])

    print(basic_info["article"]["titleString"])
    # is special issue
    print(basic_info["article"]["publication-content"]["isSpecialIssue"])
    print(basic_info["article"]["vol-first"])
    print(basic_info["article"]["volRange"])


def get_article_volume_urls_of_journals(journal_urls):
    article_volumes = dict()
    for journal_name, journal_url in journal_urls.items():
        article_volumes[journal_name] = dict()
        req = requests.get(journal_url, headers=HEADER)
        txt = req.text
        soup = BeautifulSoup(txt, features="lxml")
        journal_title = soup.head.title.string[6:]

        body = soup.body
        body_main = body.find("div", id="main")

        for child in body_main.children:
            if child.name == "ul":
                for c_child in child.children:
                    if type(c_child) == bs4.element.NavigableString:
                        pass
                    elif type(c_child) == bs4.element.Tag:
                        volume_url = c_child.a["href"]    
                        volume_info = c_child.a.string
                        article_volumes[journal_title][volume_info] = volume_url


def get_artile_urls_in_volume():
    url = "https://dblp.uni-trier.de/db/journals/access/access9.html"
    req = requests.get(url, headers=HEADER)
    txt = req.text




# get_all_journal_names()
journal_urls = get_journal_urls_from_local_file()
get_article_volume_urls_of_journals(journal_urls)







