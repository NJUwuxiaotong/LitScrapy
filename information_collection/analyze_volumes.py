import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import json
import requests

from databases.db_engine import engine, session

import bs4
from bs4 import BeautifulSoup

from sqlalchemy import distinct

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from constants import constant as const
from information_collection.http_engine import HEADER
from table_mapping.journal_volumes import Volume
from table_mapping.paper_info import Paper


def query_volumes_by_filter(conditions, limit_num=1000):
    query = session.query(Volume).filter(conditions).limit(limit_num)
    return query


def query_volumes():
    volumes = session.query(Volume.issn).distinct().all()

    print(len(volumes))

    #updated_volumes = list()
    #for volume in volumes:
    #    updated_volumes.append({const.VOLUME_ID: volume.id, 
    #                            const.VOLUME_URL: volume.url})
    #return updated_volumes


def query_journal_is_in_volumes(journal_issn):
    result = session.query(Volume).filter(Volume.issn == journal_issn).first()
    if result:
        return True
    else:
        return False


def set_updated_status_of_volumes(volume_id):
    volume = session.query(Volume).filter(Volume.id == volume_id).first()
    volume.is_updated = True
    session.commit()


def get_paper_bibtex(paper_bibtex_url):
 #   paper_bibtex_url = \
 #       const.DBLP_JOURNAL_BIBTEX_PREVIX + paper_id + \
 #       const.DBLP_JOURNAL_BIBTEX_SUFFIX

    req = requests.get(paper_bibtex_url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    paper_bibtex = soup.find("pre", {"class": "verbatim select-on-click"})

    if paper_bibtex:
        paper_bibtex = paper_bibtex.string
        bib_parser = BibTexParser()
        bib_parser.customization = convert_to_unicode
        bib_data = bp.loads(paper_bibtex, parser = bib_parser)
        return bib_data.entries[0]
    else:
        return dict()


def update_year_of_volumes():
    volumes = session.query(Volume).filter(Volume.id >= 34745)
    for volume in volumes:
        volume_id = volume.id

        paper_info = session.query(Paper)\
            .filter(Paper.volume_id == volume_id).first()
        if not paper_info:
            continue

        paper_dblp_id = paper_info.dblp_id

        paper_bibtex_url = \
            const.DBLP_JOURNAL_BIBTEX_PREVIX + paper_dblp_id + \
            const.DBLP_JOURNAL_BIBTEX_SUFFIX

        per_bibtex = get_paper_bibtex(paper_bibtex_url)
        volume_year = per_bibtex.get("year")
        volume_info = per_bibtex.get("volume")

        volume.year = volume_year
        volume.volume = volume_info
        session.commit()


update_year_of_volumes()
