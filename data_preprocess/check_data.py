from databases.db_engine import session

from constants import constant as const
from table_mapping.journal_info import Journal


class JournalPreProcess(object):
    def __init__(self):
        pass

    def check_dblp_address(self):
        dblp_addresses = session.query(Journal.dblp_address)
        num = 0
        for dblp_address in dblp_addresses:
            if const.DBLP_JOURNAL_PREVIX in dblp_address[0]:
                print(dblp_address[0])
                num = num + 1
        print(num)


test = JournalPreProcess()
test.check_dblp_address()
