
from constants import constant as const

from databases.db_engine import engine, session

from information_collection import analyze_journal
from information_collection import analyze_journal_urls
from information_collection import analyze_papers
from information_collection import analyze_volumes

from information_collection.journal_info import Journal
from information_collection.journal_volumes import Volume

from publish_lib import generate_random


except_journals = ["https://dblp.uni-trier.de/db/journals/iacr/"]


def collect_journals():
    analyze_journal_urls.get_all_journal_urls()
    journal_urls = analyze_journal_urls.get_journal_urls_from_local_file()
    print(journal_urls)
    for journal_url in journal_urls:
        soup = analyze_journal.get_journal_http_body(journal_url)
        journal_title = analyze_journal.get_journal_title(soup)
        
        journal = analyze_journal.find_journal_by_title(journal_title)
        if journal is None:
            try:
                journal_issn = analyze_journal.get_journal_issn(soup)
            except:
                journal_issn = "issn:" + generate_random.generate_random_str()
            analyze_journal.insert_journal_into_db(journal_title, journal_url, journal_issn)


def collect_journal_volumes():
    journals = analyze_journal.get_all_journals_from_db()

    for journal in journals:
        journal_issn = journal.issn
        journal_dblp_addr = journal.dblp_address
        new_journal_volumes = list()

        soup = analyze_journal.get_journal_http_body(journal_dblp_addr)
        volumes = analyze_journal.get_paper_volumes_of_journal(soup, journal_dblp_addr)
        for volume in volumes:
            volume_existence = analyze_journal.find_volume_by_url(volume[const.VOLUME_URL])
            if volume_existence is None:
                volume[const.VOLUME_UPDATED] = False
                new_journal_volumes.append(volume)

        analyze_journal.insert_volumes_into_db(new_journal_volumes, journal_issn)


def collect_journal_papers():
    while True:
        conditions = (Volume.is_updated==False)

        query = analyze_volumes.query_volumes_by_filter(conditions)
   
        for q in query:
            if "2169-3536" == q.issn:
                continue

            papers = analyze_papers.analyze_papers_of_volume(q.url)
            print(papers)
            # analyze_papers.insert_papers_into_db(papers)
            # analyze_volumes.set_updated_status_of_volumes(q.id)



collect_journal_papers()




