import json
import requests

from databases.db_engine import engine, session

import bs4
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from constants import constant as const
from information_collection.http_engine import HEADER
from information_collection.journal_volumes import Volume


def query_volumes_by_filter(conditions, limit_num=100):
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


def set_updated_status_of_volumes(volume_id):
    volume = session.query(Volume).filter(Volume.id == volume_id).first()
    volume.is_updated = True
    session.commit()

