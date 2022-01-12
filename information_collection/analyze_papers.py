import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import json
import requests

import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from databases.db_engine import engine, session
from constants import constant as const
from information_collection.http_engine import HEADER
# from information_collection.journal_volumes import Volume
from information_collection.paper_info import Paper


def get_paper_vol_and_no(paper_info):
    header = paper_info.find("h2")
    if not header:
        return None

    header = paper_info.h2.string
    if 'Volume' in header:   # get volume
        start_pos = header.find("Volume")
        end_pos = header.find(',', start_pos)
        volume = header[start_pos+6: end_pos].strip()
    else:
        volume = "None"

    if 'Number' in header:  # get number
        start_pos = header.find("Number")
        end_pos = header.find(',', start_pos)
        number = header[start_pos+6: end_pos].strip()
    else:
        number = "None"

    date = header[header.rfind(",")+1:].strip()
    return (volume, number, date)


def get_paper_bibtex(paper_id):
    paper_bibtex_url = const.DBLP_JOURNAL_BIBTEX_PREVIX + paper_id + const.DBLP_JOURNAL_BIBTEX_SUFFIX
    req = requests.get(paper_bibtex_url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    paper_bibtex = soup.find("pre", {"class": "verbatim select-on-click"})
    if paper_bibtex:
        paper_bibtex = paper_bibtex.string
        bib_parser = BibTexParser()
        bib_parser.customization = convert_to_unicode
        bib_data = bp.loads(paper_bibtex, parser = bib_parser)
        return bib_data[0]
    else:
        return None
    

def get_paper_authors(paper_info):
    """
    return a list of authors
    """
    authors = list()
    author_siblings = paper_info.find_all("span", {"itemprop": "author"})    

    for author_sibling in author_siblings:
        author_title = author_sibling.span['title']
        author_name = author_sibling.span.string
        try:
            author_dblp_url = author_sibling.a['href']
        except:
            author_dblp_url = ""
        authors.append({"author_title": author_title,
                        "author_name": author_name,
                        "author_dblp_url": author_dblp_url})
        author_sibling = author_sibling.find_next_sibling()
    return authors


def get_paper_title(paper_info):
    return paper_info.find("span", {"class": "title", "itemprop": "name"}).string


def get_paper_doi(paper_info):
    doi_url = paper_info.find("li", {"class": "ee"}).a["href"]
    return doi_url[const.DOI_URL_PREFIX_LEN:]


def analyze_papers_of_volume(url):
    info_of_papers = list()

    req = requests.get(url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    body = soup.body

    sibling = body.find("ul", class_="publ-list")

    if sibling is None:
        return info_of_papers
    
    # sibling = body_main.find_previous_sibling()
    while sibling:
        article_entries = sibling.find_all("li", {"class": "entry article"})    
        if not len(article_entries):
            sibling = sibling.find_next_sibling()
            continue

        for article_entry in article_entries:
            paper_id = article_entry["id"]

            paper_bibtex = get_paper_bibtex(paper_id)
            if paper_bibtex:
                paper_volume = paper_bibtex["volume"] 
                paper_number = paper_bibtex["number"]
                paper_year = paper_bibtex["year"]
                paper_doi = paper_bibtex["doi"]
                paper_pages = paper_bibtex["pages"]
            else:
                pass

            paper_authors = get_paper_authors(article_entry)
            paper_title = get_paper_title(article_entry)
            paper_doi = get_paper_doi(article_entry)

            info_of_papers.append({const.PAPER_AUTHOR: paper_authors, 
                                   const.PAPER_TITLE: paper_title,
                                   const.PAPER_DOI: paper_doi,
                                   const.PAPER_VOLUME: volume,
                                   const.PAPER_NUMBER: number,
                                   const.PAPER_DATE: date})
    
        sibling = sibling.find_next_sibling()
    return info_of_papers




def insert_papers_into_db(papers_info):
    papers = list()
    for paper_info in papers_info:
        # papers.append(Paper(title=, journal_issn=, ))
        pass
    session.adds(papers)
    session.commit()




#x = "https://dblp.uni-trier.de/db/journals/isafm/isafm23.html"
x = "https://dblp.org/db/journals/jsjkx/jsjkx47.html"
analyze_papers_of_volume(x)

