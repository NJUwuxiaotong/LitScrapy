
from constants import constant as const

from databases.db_engine import engine, session

from information_collection import analyze_journal
from information_collection import analyze_journal_urls
from information_collection import analyze_papers
from information_collection import analyze_volumes

from table_mapping.author_info import Author
from table_mapping.journal_info import Journal
from table_mapping.journal_volumes import Volume
from table_mapping.paper_info import Paper
from table_mapping.paper_author_mapping import PaperAuthor

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
            analyze_journal.insert_journal_into_db(
                    journal_title, journal_url, journal_issn)


def collect_journal_volumes():
    journals = analyze_journal.get_all_journals_from_db()

    for journal in journals:
        journal_issn = journal.issn
        journal_dblp_addr = journal.dblp_address
        new_journal_volumes = list()

        soup = analyze_journal.get_journal_http_body(journal_dblp_addr)
        volumes = analyze_journal.get_paper_volumes_of_journal(
                soup, journal_dblp_addr)
        for volume in volumes:
            volume_existence = analyze_journal.find_volume_by_url(
                    volume[const.VOLUME_URL])
            if volume_existence is None:
                volume[const.VOLUME_UPDATED] = False
                new_journal_volumes.append(volume)

        analyze_journal.insert_volumes_into_db(
                new_journal_volumes, journal_issn)


def collect_journal_papers():
    while True:
        conditions = (Volume.is_updated==False)
        new_volumes = analyze_volumes.query_volumes_by_filter(
                conditions, limit_num=10)
  

        for new_volume in new_volumes:
            volume_id = new_volume.id
            journal_issn = new_volume.issn
            
            new_papers = analyze_papers.analyze_papers_of_volume(
                    new_volume.url)
                
            # analyze_papers.insert_papers_into_db(papers)
            new_db_papers = list()
            new_db_authors = list()
                
            for new_paper in new_papers:
                new_db_papers.append(
                        Paper(title=new_paper[const.PAPER_TITLE], 
                            journal_issn=new_volume.issn, 
                            volume_id=new_volume.id, 
                            volume=new_paper[const.PAPER_VOLUME], 
                            number=new_paper[const.PAPER_NUMBER],
                            start_page=new_paper[const.PAPER_START_PAGE], 
                            end_page=new_paper[const.PAPER_END_PAGE],                                 year=new_paper[const.PAPER_DATE], 
                            url=new_paper[const.PAPER_URL], 
                            doi=new_paper[const.PAPER_DOI]))
                    
                import pdb;pdb.set_trace()

                # add authors
                authors = new_paper[const.PAPER_AUTHOR]
                for author in authors:
                    author_title = author["author_title"]
                    author_name = author["author_name"]
                    author_dblp_url = author["author_dblp_url"]




                # add papers
                # session.adds()

                # add authors
                # session.adds()
                
                # update volume
                #analyze_volumes.set_updated_status_of_volumes(q.id)

                # session.commit()
            #except:
            #    print("Being processing volume [%s]" % volume_id)
            #    exit(1)


collect_journal_papers()

