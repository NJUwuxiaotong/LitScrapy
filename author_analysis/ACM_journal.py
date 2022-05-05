import json
import re
import requests

import bs4
from bs4 import BeautifulSoup

from information_collection.http_engine import HEADER


paper_url = "https://dl.acm.org/doi/10.1145/3291049"

req = requests.get(paper_url, headers=HEADER)
txt = req.text
soup = BeautifulSoup(txt, features="lxml")

print(soup)
