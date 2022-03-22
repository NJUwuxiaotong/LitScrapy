from sqlalchemy import func

from constants import constant as const

from databases.db_engine import engine, session

from sqlalchemy import distinct

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

        if analyze_volumes.query_journal_is_in_volumes(journal_issn):
            continue

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

    arx_journal_issn = "2331-8422"

#    while True:
    # conditions = (Volume.is_updated == False)

    volume_id = 46770

    while volume_id <= 46770:

        conditions = (Volume.id == volume_id)
        new_volumes = analyze_volumes.query_volumes_by_filter(
                conditions)                           #, limit_num=5)

        new_volume_infos = list()
        for new_volume in new_volumes:
             new_volume_infos.append(
                 {const.VOLUME_ID: new_volume.id,
                  const.JOURNAL_ISSN: new_volume.issn,
                  const.VOLUME_URL: new_volume.url})

     #   if not new_volume_infos:
     #       print("Finish the update!")
     #       break

        for new_volume_info in new_volume_infos:

            if new_volume_info[const.JOURNAL_ISSN] == arx_journal_issn:
                continue

            print("%s" % new_volume_info[const.VOLUME_URL])
            print("VOLUME ID: %s" % new_volume_info[const.VOLUME_ID])

            # if new_volume_info[const.VOLUME_ID] in [35956, 35957, 44428,
            #                                        44429, 44430]:
            #    continue

            new_paper_infos = analyze_papers.analyze_papers_of_volume(
                    new_volume_info[const.VOLUME_URL])

            for new_paper_info in new_paper_infos:
                paper_query = \
                    session.query(Paper).filter(
                        Paper.dblp_id == new_paper_info[const.PAPER_DBLP_ID])\
                        .first()

                if paper_query is not None:
                    print("Database has the record [dblp_id: %s]" %
                          paper_query.dblp_id)
                    continue
                else:
                    print("Database has no record [dblp_id: %s]" %
                          new_paper_info[const.PAPER_DBLP_ID])

                new_paper = Paper(
                    title=new_paper_info[const.PAPER_TITLE],
                    journal_issn=new_volume_info[const.JOURNAL_ISSN],
                    volume_id=new_volume_info[const.VOLUME_ID],
                    volume=new_paper_info[const.PAPER_VOLUME],
                    number=new_paper_info[const.PAPER_NUMBER],
                    start_page=new_paper_info[const.PAPER_START_PAGE],
                    end_page=new_paper_info[const.PAPER_END_PAGE],
                    year=new_paper_info[const.PAPER_DATE],
                    url=new_paper_info[const.PAPER_URL],
                    doi=new_paper_info[const.PAPER_DOI],
                    dblp_id=new_paper_info[const.PAPER_DBLP_ID])
                session.add(new_paper)
                session.flush()
                session.refresh(new_paper)
                new_paper_id = new_paper.id

                # add authors
                author_infos = new_paper_info[const.PAPER_AUTHOR]
                order = 1
                for author_info in author_infos:
                    author_query = \
                        session.query(Author).filter(
                            Author.title == author_info["author_title"]).first()
                    if author_query:
                        author_id = author_query.id
                    else:
                        new_author = Author(
                            title=author_info["author_title"],
                            name=author_info["author_name"],
                            dblp_url=author_info["author_dblp_url"])

                        session.add(new_author)
                        session.flush()
                        session.refresh(new_author)
                        author_id = new_author.id

                    session.add(PaperAuthor(
                        paper_id=new_paper_id,
                        author_id=author_id,
                        order=order))
                    order += 1
                session.commit()

            volume = \
                session.query(Volume).filter(
                    Volume.id == new_volume_info[const.VOLUME_ID]).first()
            volume.is_updated = True
            session.commit()
            print("Volume - [ID: %s] has been processed!" %
                  new_volume_info[const.VOLUME_ID])

        volume_id = volume_id + 1


def update_is_updated_of_volumes():
    paper_volume_ids = session.query(distinct(Paper.volume_id))
    volume_ids = session.query(Volume.id).filter(Volume.id.notin_(paper_volume_ids)).all()

    for volume_id in volume_ids:
        session.query(Volume).filter(Volume.id == volume_id[0]).update(
            {Volume.is_updated: False})

    session.commit()
    session.close()


collect_journal_papers()
