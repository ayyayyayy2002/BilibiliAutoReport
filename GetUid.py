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
list_file = os.path.join(base_dir, '附加文件', 'list.txt')
white_file = os.path.join(base_dir, '附加文件', 'white.txt')
black_file = os.path.join(base_dir, '附加文件', 'black.txt')
keywords_file = os.path.join(base_dir, '附加文件', 'keywords.txt')
log_path = os.path.join(base_dir, '运行记录')
########################################################################################################################
uid_file = os.path.join(base_dir, '附加文件', 'uid.txt')
env_file = os.path.join(base_dir, '附加文件', '.env')
proxies = {'http': None, 'https': None}
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
with open(keywords_file, 'r', encoding='utf-8') as f:
    for line in f:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith('#'):  # 排除空行和以“#”开头的行
            keywords.add(stripped_line)




base_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(base_dir, '附加文件', 'User Data')
chrome_binary_path = os.path.join(base_dir, '附加文件', 'chrome-win', 'chrome.exe')
chrome_driver_path = os.path.join(base_dir, '附加文件',  'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument("--headless")
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")
options.add_argument('log-level=3')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome( service = service, options=options)  # 启动 Chrome 浏览器
driver.set_window_size(1000, 700)  # 设置浏览器窗口大小（宽度, 高度）



for keyword in keywords:  # 遍历关键词列表，进行搜索和处理
    default = f'https://search.bilibili.com/video?keyword={quote(keyword)}&from_source=video_tag'
    driver.get(default)
    elements = driver.find_elements(By.XPATH,"//*[@id='i_cecream']/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/a")
    uid_list.clear()
    count = 0
    for element in elements:
        href = element.get_attribute("href")
        match = re.search(r"space.bilibili.com/(\d+)", href)  # 在 href 中搜索匹配的内容
        if not match:
            continue
        uid = match.group(1)  # 获取匹配到的UID部分
        uids.add(uid)
        uid_list.add(uid)  # 添加 UID 到集合中
        count += 1
        if count >= 30:
            break
    print(f'\n关键词：{keyword}  默认排序结果：\n{uid_list}')
    with open(uid_file, 'a', encoding='utf-8') as f:
        f.write(f'\n关键词：{keyword}  默认排序结果：\n{uid_list}')
    print(default)


    pubdate = f'https://search.bilibili.com/video?keyword={quote(keyword)}&from_source=video_tag&order=pubdate'
    driver.get(pubdate)
    elements = driver.find_elements(By.XPATH,"//*[@id='i_cecream']/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/a")
    uid_list.clear()
    count = 0
    for element in elements:
        href = element.get_attribute("href")
        match = re.search(r"space.bilibili.com/(\d+)", href)  # 在 href 中搜索匹配的内容
        if not match:
            continue
        uid = match.group(1)  # 获取匹配到的UID部分
        uids.add(uid)
        uid_list.add(uid)  # 添加 UID 到集合中
        count += 1
        if count >= 30:
            break
    print(f'\n关键词：{keyword}  时间排序结果：\n{uid_list}')
    with open(uid_file, 'a', encoding='utf-8') as f:
        f.write(f'\n关键词：{keyword}  时间排序结果：\n{uid_list}')
    print(pubdate)



try:
    # 获取当前时间并格式化
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = os.path.join(log_path, f'{timestamp}.txt')
    shutil.copy(uid_file, backup_filename)
    print(f"成功保存备份：{backup_filename}")
except IOError as e:
    print(f"保存备份时发生错误：{e}")



cookies = driver.get_cookies()
COOKIE = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
UA = driver.execute_script("return navigator.userAgent;")
CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)
load_dotenv(dotenv_path=env_file)
os.environ['UA'] = UA
os.environ['COOKIE'] = COOKIE
set_key(env_file, 'UA', UA)
set_key(env_file, 'COOKIE', COOKIE)
COOKIE2 = os.getenv('COOKIE2')



if COOKIE2:
    CSRF2 = re.search(r'bili_jct=([^;]*)', COOKIE2).group(1)
    headers = {'cookie': COOKIE2, 'user-agent': UA}
    response = requests.get('https://api.bilibili.com/x/v2/history/toview', headers=headers, proxies=proxies)
    data = response.json()
    for item in data['data']['list']:
        mid = item['owner']['mid']
        uids.add(mid)
        print(mid)
    data = {'csrf': CSRF2}
    response = requests.post('https://api.bilibili.com/x/v2/history/toview/clear', headers=headers, data=data,proxies=proxies)
    print(response.text)




headers = {'cookie': COOKIE, 'user-agent': UA}
response = requests.get('https://api.bilibili.com/x/v2/history/toview',  headers=headers,proxies= proxies)
data = response.json()
for item in data['data']['list']:
    mid = item['owner']['mid']
    uids.add(mid)
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

