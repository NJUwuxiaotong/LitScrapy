import urllib.request

import random

url = "https://dl.acm.org/doi/10.1145/3291049"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
          "Connection": "close"#, "Referer": "https://dl.acm.org/"
          }

proxy_list = [
    {"http": "61.135.217.7:8765"},
    {"http": "111.155.116.245:8765"},
    {"http": "122.114.31.177:8765"},
]

# 随机选择一个代理
proxy = random.choice(proxy_list)

# 使用选择的代理构建代理处理器对象
httpproxy_handler = urllib.request.ProxyHandler(proxy)
opener = urllib.request.build_opener(httpproxy_handler)
request = urllib.request.Request(url, headers=header)
response = opener.open(request)
print(response.read().decode('utf-8'))
