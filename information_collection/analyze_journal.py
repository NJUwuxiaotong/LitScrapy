import json
import requests

from databases.db_engine import engine, session

import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from constants import constant as const
from information_collection.http_engine import HEADER
from table_mapping.journal_info import Journal
from table_mapping.journal_volumes import Volume
from table_mapping.press_info import Press


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
    session.add(
            Journal(name=journal_title, dblp_address=journal_addr, issn=issn))
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
                if type(c_child) == bs4.element.NavigableString:
                    pass
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


def get_presses():
    press_url = "https://dblp.uni-trier.de/db/journals/publ/index.html"
    req = requests.get(press_url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    press_soup = soup.find("div", "clear-both")
    press_soup = press_soup.find_next_sibling()
    press_list = press_soup.find_all("li")

    presses = dict()
    for press in press_list:
        press_name = press.a.string
        press_url = press.a["href"]
        presses[press_name] = press_url
        session.add(Press(name=press_name, url=press_url))

    session.commit()
    session.close()


def find_press_of_journal():
    presses = session.query(Press)
    for press in presses:
        press_id = press.id
        press_url = press.url

        req = requests.get(press_url, headers=HEADER)
        txt = req.text
        soup = BeautifulSoup(txt, features="lxml")
        press_soup = soup.find("div", "clear-both")
        press_soup = press_soup.find_next_sibling()
        press_soup = press_soup.find_next_sibling()
        p_infos = press_soup.find_all("li")

        while p_infos:
            for p_info in p_infos:
                journal_url = p_info.a["href"]
                if const.DBLP_JOURNAL_PREVIX in journal_url:
                    journal_url = journal_url[:-10]
                    j_q = session.query(Journal)\
                        .filter(Journal.dblp_address == journal_url).first()
                    if j_q:
                        j_q.press = press_id
                        session.commit()

            press_soup = press_soup.find_next_sibling()
            p_infos = press_soup.find_all("li")
    session.close()


def check_journal_press(journal_url):
    journal_query = session.query(Journal)\
        .filter(Journal.dblp_address == journal_url).first()

    if journal_query:
        return True
    else:
        return False


find_press_of_journal()
