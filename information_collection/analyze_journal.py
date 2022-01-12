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


def get_journal_title(soup):
    return soup.head.title.string[6:]


def get_journal_issn(soup):
    body = soup.body
    body_main = body.find("div", id="main")
    body = body_main.find("em", text="issn:")
    body = body.find_next_siblings()[0]
    return body.string


def insert_journal_into_db(journal_title, journal_addr, issn):
    session.add(Journal(name=journal_title, dblp_address=journal_addr, issn=issn))
    session.commit()


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
                        volume_year = 0
                        #if "volume" in volume_info.lower():
                        #    volume_number, volume_year =  volume_info.split(":")
                        #    volume_number = volume_number[7:].strip()
                        #    volume_year = volume_year.strip()
                        # else:
                        #    volume_number = volume_info
                        #    volume_year = 0

                        article_volumes.append(
                            {const.VOLUME_NUMBER: volume_info,
                             const.VOLUME_YEAR: volume_year,
                             const.VOLUME_URL: volume_url})
    return article_volumes


def insert_volumes_into_db(volumes, issn):
    new_volumes = list()
    for volume in volumes:
        new_volumes.append(Volume(
            issn=issn, 
            volume=volume[const.VOLUME_NUMBER], 
            year=volume[const.VOLUME_YEAR],
            url=volume[const.VOLUME_URL],
            is_updated=volume[const.VOLUME_UPDATED]
            ))
    session.add_all(new_volumes)
    session.commit()


def get_journal_http_body(journal_url):
    req = requests.get(url=journal_url, headers=HEADER)
    soup = BeautifulSoup(req.text, features="lxml")
    return soup


def find_journal_by_issn(journal_issn):
    return session.query(Journal).filter(Journal.issn == journal_issn).first()


def find_journal_by_title(journal_title):
    return session.query(Journal).filter(Journal.name == journal_title).first()


def get_all_journals_from_db():
    return session.query(Journal).all()


def find_volume_by_url(volume_url):
    return session.query(Volume).filter(Volume.url == volume_url).first()



