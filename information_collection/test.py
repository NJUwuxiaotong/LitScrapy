import json
import requests

from databases.db_engine import engine, session

import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from constants import constant as const
from information_collection.http_engine import HEADER
from information_collection.journal_info import Journal
from information_collection.journal_volumes import Volume


JOURNAL_URLS_FILE = "./journal_urls.json"


def get_paper_volumes_of_journal(soup, journal_url):
    """
    return a list of dictionaries, including volume number, year, dblp_address
    """
    body = soup.body
    body_main = body.find("div", id="main")
    article_volumes = list()
    for child in body_main.children:
        if child.name == "ul":
            for c_child in child.children:
                if type(c_child) == bs4.element.NavigableString:                    pass
                elif type(c_child) == bs4.element.Tag:
                    volumes = c_child.find_all("a")
                    for volume in volumes:
                        volume_url = volume["href"]
                        volume_info = volume.string
                        if "volume" in volume_info.lower():
                            volume_number, volume_year =  volume_info.split(":")
                            volume_number = volume_number[7:].strip()
                            volume_year = volume_year.strip()
                        else:
                            volume_number = volume_info
                            volume_year = 0 
                        article_volumes.append(
                            {const.VOLUME_NUMBER: volume_number,
                             const.VOLUME_YEAR: volume_year,
                             const.VOLUME_URL: volume_url})
    return article_volumes


def get_journal_http_body(journal_url):
    req = requests.get(url=journal_url, headers=HEADER)
    soup = BeautifulSoup(req.text, features="lxml")
    return soup


url = "https://dblp.uni-trier.de/db/journals/sigaccess/"
soup = get_journal_http_body(url)
print(get_paper_volumes_of_journal(soup, url))
