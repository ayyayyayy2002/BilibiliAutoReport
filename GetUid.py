import shutil
from datetime import datetime
from urllib.parse import quote

from dotenv import load_dotenv, set_key
import requests
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
list_file = os.path.join(base_dir, '附加文件', 'list')
white_file = os.path.join(base_dir, '附加文件', 'white')
black_file = os.path.join(base_dir, '附加文件', 'black')
########################################################################################################################
uid_file = os.path.join(base_dir, '附加文件', 'uid.txt')
env_file = os.path.join(base_dir, '附加文件', '.env')
proxies = {'http': None, 'https': None}
load_dotenv(dotenv_path=env_file)
COOKIE = os.getenv('COOKIE')
COOKIE2 = os.getenv('COOKIE2')
MEDIAID = os.getenv('MEDIAID')
UA = os.getenv('UA')
CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)
uids = set()
keywords = set()
uid_list = set()
lists = set()


if os.path.exists(uid_file):
    with open(uid_file, 'r', encoding='utf-8') as f:  # 以读取模式打开文件
        for line in f:
            line = line.strip()  # 去掉行首尾的空白字符
            if line:  # 如果不是空行，则认为是UID
                uids.add(line)
    os.remove(uid_file)
else:
    print(f"文件 {uid_file} 不存在，无需删除。")

with open(list_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        uid = line.strip()
        if uid.isdigit():
            uids.add(int(uid))
            lists.add(int(uid))




if COOKIE2:
    CSRF2 = re.search(r'bili_jct=([^;]*)', COOKIE2).group(1)
    headers = {'cookie': COOKIE2, 'user-agent': UA}
    response = requests.get('https://api.bilibili.com/x/v2/history/toview', headers=headers, proxies=proxies)
    data = response.json()
    for item in data['data']['list']:
        mid = item['owner']['mid']
        uids.add(int(mid))
        lists.add(int(mid))
        print(mid)
    data = {'csrf': CSRF2}
    response = requests.post('https://api.bilibili.com/x/v2/history/toview/clear', headers=headers, data=data,proxies=proxies)
    print(response.text)




headers = {'cookie': COOKIE, 'user-agent': UA}
response = requests.get('https://api.bilibili.com/x/v2/history/toview',  headers=headers,proxies= proxies)
data = response.json()
for item in data['data']['list']:
    mid = item['owner']['mid']
    uids.add(int(mid))
    lists.add(int(mid))
    print(mid)
data = {'csrf': CSRF}
response = requests.post('https://api.bilibili.com/x/v2/history/toview/clear', headers=headers, data=data,proxies=proxies)
print(response.text)



with open(white_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        uid = line.strip()
        if uid.isdigit():
            uids.add(int(uid))
            lists.add(int(uid))
with open(black_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        uid = line.strip()
        if uid.isdigit():
            uids.discard(int(uid))
            lists.discard(int(uid))



with open(uid_file, 'w', encoding='utf-8') as file:
    for uid in uids:
        #uid = int(uid)
        file.write(f'{uid}\n')
print('UID获取完成')


lists = sorted(lists)
with open(list_file, 'w', encoding='utf-8') as file:
    for list in lists:
        file.write(f'{list}\n')
