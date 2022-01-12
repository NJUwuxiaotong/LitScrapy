from databases.db_engine import engine, session

from information_collection import analyze_journal
from information_collection import analyze_journal_urls
from information_collection.journal_info import Journal

from publish_lib import generate_random


print(session.query(Journal).filter().count())
