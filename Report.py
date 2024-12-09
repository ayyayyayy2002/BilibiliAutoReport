from dotenv import load_dotenv
from datetime import datetime

from onnxruntime.tools.ort_format_model import script_dir
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Capcha import capcha
import requests
import time
import re
import os



base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, '附加文件', 'uid.txt')
log_file = os.path.join(base_dir, '运行记录', '循环记录.txt')
env_file = os.path.join(base_dir, '附加文件', '.env')
proxies = {'http': None, 'https': None}
uids = set()
load_dotenv(dotenv_path=env_file)
COOKIE = os.getenv('COOKIE')
MEDIAID = os.getenv('MEDIAID')
UA = os.getenv('UA')
CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)
########################################################################################################################

with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}开始\n')
try:
    with open(uid_file, 'r', encoding='utf-8') as file:  # 以读取模式打开文件
        for line in file:
            line = line.strip()  # 去掉行首尾的空白字符
            uids.add(line)
except Exception as e:
    print(f"无法读取UID文件: {e}")
    exit(0)



if not uids:
    print("uid.txt 文件中没有可处理的UID，程序退出")
    exit(0)






base_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(base_dir, '附加文件', 'User Data')
chrome_binary_path = os.path.join(base_dir, '附加文件', 'chrome-win', 'chrome.exe')
chrome_driver_path = os.path.join(base_dir, '附加文件', 'chromedriver.exe')
script_file = os.path.join(base_dir, '附加文件', '页面脚本','总脚本.js')
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")  # 禁用缓存
options.add_argument('log-level=3')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # 启动 Chrome 浏览器
driver.set_window_size(1000, 700)  # 设置浏览器窗口大小（宽度, 高度）
driver.get("https://space.bilibili.com")



for uid in uids:
    aids = []
    titles = []
    pics = []
    try:
        with open(uid_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(uid_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != uid:
                    f.write(line)
        print(f"删除UID: {uid}")
    except Exception as e:
        print(f"删除UID时发生错误: {e}")


    headers = {'cookie': COOKIE, 'user-agent': UA}
    search_url = f'https://api.bilibili.com/x/polymer/space/seasons_series_list?mid={uid}&page_num=1&page_size=5'
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    if data.get('data', {}).get('items_lists', {}).get('seasons_list', []):
        season_ids = [season['meta']['season_id'] for season in data.get('data', {}).get('items_lists', {}).get('seasons_list', [])]

        for season_id in season_ids:
            search_url = f'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={uid}&sort_reverse=false&season_id={season_id}&page_num=1&page_size=1'
            headers = {'cookie': COOKIE, 'user-agent': UA}
            response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
            data = response.json()
            if 'data' in data and 'archives' in data['data']:
                for archive in data['data']['archives']:
                    aids.append(archive['aid'])  # 添加 aid 到集合

    search_url = f'https://api.bilibili.com/x/series/recArchivesByKeywords?mid={uid}&keywords=&ps=1'
    headers = {'cookie': COOKIE, 'user-agent': UA}
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    for archive in data['data']['archives']:
        aids.append(archive['aid'])

    if aids and aids[0]:
        driver.get(f'https://space.bilibili.com/{uid}')
        with open(script_file, 'r', encoding='utf-8') as file:
            script = file.read()
        result = driver.execute_async_script(script)
        if '352' in result or '412' in result:
            capcha(aids[0],driver)
        else:
            continue



with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}结束\n')









