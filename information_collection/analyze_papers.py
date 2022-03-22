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
from table_mapping.paper_info import Paper


def get_paper_bibtex(paper_id):
    return dict()

    paper_bibtex_url = \
        const.DBLP_JOURNAL_BIBTEX_PREVIX + paper_id + \
        const.DBLP_JOURNAL_BIBTEX_SUFFIX
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
    return paper_info.find(
            "span", 
            {"class": "title", "itemprop": "name"}).string


def get_paper_doi(paper_info):
    doi_url = paper_info.find("li", {"class": "ee"}).a["href"]
    return doi_url[const.DOI_URL_PREFIX_LEN:]


def get_paper_start_end_pages(paper_page):
    try:
        pages = paper_page.split("--")
        return int(pages[0]), int(pages[1])
    except:
        return 0, 0


def analyze_papers_of_volume(url):
    info_of_papers = list()

    req = requests.get(url, headers=HEADER)
    txt = req.text
    soup = BeautifulSoup(txt, features="lxml")
    sibling = soup.body.find("ul", class_="publ-list")

    # import pdb; pdb.set_trace()

    if sibling is None:
        return info_of_papers
    
    # sibling = body_main.find_previous_sibling()
    paper_num = 0
    while sibling:
        # item_name = "entry article"
        item_name = "entry informal"
        article_entries = sibling.find_all("li", {"class": item_name})
        if not len(article_entries):
            sibling = sibling.find_next_sibling()
            continue

        for article_entry in article_entries:
            paper_id = article_entry["id"]

            paper_bibtex = get_paper_bibtex(paper_id)
            paper_authors = get_paper_authors(article_entry)
            #paper_title = get_paper_title(article_entry)

            paper_title = paper_bibtex.get("title")

            if paper_title is None:
                paper_title = ""

            if len(paper_title) > 255:
                paper_title = paper_title[:255]

            paper_pages = paper_bibtex.get("pages")
            start_page, end_page = get_paper_start_end_pages(paper_pages) 

            info_of_papers.append({
                const.PAPER_DBLP_ID: paper_id,
                const.PAPER_AUTHOR: paper_authors, 
                const.PAPER_TITLE: paper_title,
                const.PAPER_DOI: paper_bibtex.get("doi"),
                const.PAPER_VOLUME: paper_bibtex.get("volume"),
                const.PAPER_NUMBER: paper_bibtex.get("number"),
                const.PAPER_DATE: paper_bibtex.get("year"),
                const.PAPER_START_PAGE: start_page,
                const.PAPER_END_PAGE: end_page,
                const.PAPER_URL: paper_bibtex.get("url")})

            paper_num += 1
            if paper_num % 100 == 0:
                print("The number of papers from web [%s] is %s" %
                      (paper_num, url))

        sibling = sibling.find_next_sibling()

    print("The total number of papers from web [%s] is %s" % (paper_num, url))
    return info_of_papers


# volume_url = "https://dblp.uni-trier.de/db/journals/tinytocs/tinytocs1.html"
# info_of_papers = analyze_papers_of_volume(volume_url)
# print(info_of_papers)
