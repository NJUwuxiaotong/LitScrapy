from constants import constant
from information_collection import collect_data


command = constant.CMD_COLLECT_PAPER

if command == constant.CMD_COLLECT_JOURNAL:
    collect_data.collect_journals()
elif command == constant.CMD_COLLECT_VOLUME:
    collect_data.collect_journal_volumes()
elif command == constant.CMD_COLLECT_PAPER:
    collect_data.collect_journal_papers()
else:
    print("Command Error!")
