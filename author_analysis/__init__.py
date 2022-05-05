# coding=utf-8

import requests
import time
from lxml import etree


def spiderPage(url):
    if url is None:
        return None

    proxies = {
        'http': 'http://124.72.109.183:8118',
    }

# 'http://49.85.1.79:31666'


    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400'

    headers = {'User-Agent': user_agent}
    htmlText = requests.get(url, headers=headers, proxies=proxies).text

    print(htmlText)


url = "https://dl.acm.org/doi/10.1145/3291049"
spiderPage(url)
