import json
import os
import requests
import time

import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


from constants import constant as const
from information_collection.http_engine import HEADER


JOURNAL_URLS_FILE = "./journal_urls.json"
except_journals = ["https://dblp.uni-trier.de/db/journals/iacr/"]


def get_all_journal_urls():
    paper_urls = list()
    start_num = 0
    while True:
        target = const.DBLP_SOURCE_URL + "?pos=" + str(start_num)
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
            # journal_name = l_link.string
            paper_url = l_link["href"].strip()
            if paper_url not in paper_urls and paper_url not in except_journals:
                paper_urls.append(paper_url)
        start_num = start_num + const.DBLP_JOURNAL_NUM_PER_PAGE

    with open(JOURNAL_URLS_FILE, "w") as f:
        json.dump(paper_urls, f)


def get_journal_urls_from_local_file():
    try:
        with open(JOURNAL_URLS_FILE, "r") as f:
            journal_urls = json.load(f)
        return journal_urls
    except FileNotFoundError:
        print("File [%s] does not exist!" % JOURNAL_URLS_FILE)
        exit(1)

