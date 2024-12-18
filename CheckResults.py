import os
import re

import requests
from dotenv import load_dotenv
proxies = {'http': None, 'https': None}
base_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(base_dir, '附加文件', '.env')
bvid_file = os.path.join(base_dir, '附加文件', 'bvid.txt')
load_dotenv(dotenv_path=env_file)
bvids = []
deleted = []
restricted = []
handled = []
normal = []






UA = os.getenv('UA')
COOKIE = os.getenv('COOKIE1')
CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)
headers = {'cookie': COOKIE, 'user-agent': UA}
params = {
    'csrf': [
        CSRF,
        CSRF,
    ],
    'page_size': '3000',
    'build': '0',
    'mobi_app': 'web',
}
while True:
    try:
        response = requests.get('https://message.bilibili.com/x/sys-msg/query_user_notify',params=params,headers=headers,proxies=proxies)
        data = response.json()

        for item in data["data"]["system_notify_list"]:
            bvid = item["content"].split("【")[1].split("】")[0]
            bvids.append(bvid)
            if "下线" in item["content"]:
                deleted.append(bvid)
            elif "限制流量分发" in item["content"]:
                restricted.append(bvid)
            elif "已被处理" in item["content"]:
                handled.append(bvid)
            else:
                normal.append(bvid)
        break

    except Exception as e:
        print(e)

with open(bvid_file, 'w', encoding='utf-8') as file:
    print(f'总数: {len(bvids)} 下线: {len(deleted)} 限流: {len(restricted)} 其他处理: {len(handled)}')
    file.write(f'总数: {len(bvids)} 下线: {len(deleted)} 限流: {len(restricted)} 其他处理: {len(handled)} \n')
    file.write(f'\n下线 {100*len(deleted)/len(bvids)}%\n')
    for bvid in deleted:
        file.write(f'{bvid}\n')
    file.write(f'\n限流 {100*len(restricted)/len(bvids)}%\n')
    for bvid in restricted:
        file.write(f'{bvid}\n')
    file.write(f'\n其他处理 {100*len(handled)/len(bvids)}%\n')
    for bvid in handled:
        file.write(f'{bvid}\n')