import json
import re
import requests

import bs4
from bs4 import BeautifulSoup

from information_collection.http_engine import HEADER


paper_url = "https://ieeexplore.ieee.org/document/7920335"

req = requests.get(paper_url, headers=HEADER)
txt = req.text
soup = BeautifulSoup(txt, features="lxml")

pattern = re.compile(r'xplGlobal.document.metadata=(.*?);',
                     re.MULTILINE | re.DOTALL)
script = soup.find("script", text=pattern)
res_dic = pattern.search(script.string).group(1)
json_data = json.loads(res_dic)
print(json_data["authors"])

result = [
    {'name': 'Xiaotong Wu',
     'affiliation': ['State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, P.R. China'],
     'bio': {'graphic': '/mediastore_new/IEEE/content/freeimages/6687317/9510182/7920335/wu-2701817-small.gif', 'p': ['Xiaotong Wu received the bachelor’s degree in software engineering from Central South University and the master’s degree in software engineering from the Department of Computer Science and Technology, Nanjing University of China. He is currently working toward the PhD degree in the Department of Computer Science and Technology, Nanjing University, China. His research interests include data privacy, network security, cloud computing, and big data. He is a student member of the IEEE.']},
     'firstName': 'Xiaotong',
     'lastName': 'Wu',
     'orcid': '0000-0003-3262-9420',
     'id': '37085855169'},
    {'name': 'Taotao Wu',
     'affiliation': ['State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, P.R. China'], 'bio': {'graphic': '/mediastore_new/IEEE/content/freeimages/6687317/9510182/7920335/twu-2701817-small.gif', 'p': ['Taotao Wu received the BS degree in computer science from the Nanjing University of Science and Technology, Nanjing, China. He is currently working toward the PhD degree in the Department of Computer Science and Technology, Nanjing University, Nanjing, China. His research interests include cloud computing and applications multimedia computing, and communications social computing. He is a student member of the IEEE.']},
     'firstName': 'Taotao',
     'lastName': 'Wu',
     'orcid': '0000-0001-7939-3609', 'id': '37085855699'},
    {'name': 'Maqbool Khan', 'affiliation': ['State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, P.R. China'], 'bio': {'graphic': '/mediastore_new/IEEE/content/freeimages/6687317/9510182/7920335/khan-2701817-small.gif', 'p': ['Maqbool Khan received BSc and MSc degrees in computer science from Gomal University D.I. Khan Pakistan, in 2002 and 2004, respectively, and the MS degree in information security from Huazhong University of Science and Technology Wuhan, China, in 2013. He worked as a lecturer in the Govt. College Abbottabad, Pakistan. He won the cultural scholarship award for abroad study from Ministry of Education Pakistan. Currently, he is working toward the PhD in the Department of Computer Science and Technology, Nanjing University, China. His research interests include big data, massive graphs, and cloud computing. He is a student member of the IEEE.']}, 'firstName': 'Maqbool', 'lastName': 'Khan', 'id': '37085795952'}, {'name': 'Qiang Ni', 'affiliation': ['School of Computing and Communications, Lancaster University, Lancaster, United Kingdom'], 'bio': {'graphic': '/mediastore_new/IEEE/content/freeimages/6687317/9510182/7920335/ni-2701817-small.gif', 'p': ['Qiang Ni received the PhD degree in engineering from Huazhong University of Science and Technology, Wuhan, in 1999. He is a full professor and the head of Communication Systems Group, School of Computing and Communications, Lancaster University, United Kingdom. He is with Data Science Institute and Security Lancaster Centre. His research interests include future generation communications and networking systems, big data analytics, mobile and cloud networks, 5G, SDN, security and privacy, etc. Up to now, he had published more than 180 research papers in international journals and conferences. He is a senior member of the IEEE.']}, 'firstName': 'Qiang', 'lastName': 'Ni', 'orcid': '0000-0002-4593-1656', 'id': '37266488500'}, {'name': 'Wanchun Dou', 'affiliation': ['State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, P.R. China'], 'bio': {'graphic': '/mediastore_new/IEEE/content/freeimages/6687317/9510182/7920335/dou-2701817-small.gif', 'p': ['Wanchun Dou received the PhD degree in mechanical and electronic engineering from Nanjing University of Science and Technology, China, in 2001. From Apr. 2001 to Dec. 2002, he did his postdoctoral research in the Department of Computer Science and Technology, Nanjing University, China. Now, he is a full professor of the State Key Laboratory for Novel Software Technology, Nanjing University, China. From Apr. 2005 to Jun. 2005 and from Nov. 2008 to Feb. 2009, he respectively visited the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, as a visiting scholar. Up to now, he has chaired three NSFC projects and published more than 60 research papers in international journals and international conferences. His research interests include workflow, cloud computing and service computing. He is a member of the IEEE.']}, 'firstName': 'Wanchun', 'lastName': 'Dou', 'orcid': '0000-0003-4833-2023', 'id': '37547250700'}]

