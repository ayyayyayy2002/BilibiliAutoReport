import os
import re

import requests
from dotenv import load_dotenv
proxies = {'http': None, 'https': None}
base_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(base_dir, '附加文件', '.env')
bvid_file = os.path.join(base_dir, '附加文件', 'bvid.txt')
load_dotenv(dotenv_path=env_file)
while True:
    try:
        N = int(input("请输入要查看的账号编号:"))
        print(f"读取到: {N}")
        break
    except ValueError:
        print("无效输入。")



cookie_name = f'COOKIE{N}'  # 使用格式字符串生成变量名
UA = os.getenv('UA')
COOKIE = os.getenv(cookie_name)
CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)
headers = {'cookie': COOKIE, 'user-agent': UA}
params = {
    'csrf': [
        CSRF,
        CSRF,
    ],
    'page_size': '1000',
    'build': '0',
    'mobi_app': 'web',
}

response = requests.get('https://message.bilibili.com/x/sys-msg/query_user_notify',params=params,headers=headers,proxies=proxies)
data = response.json()
print(response.text)
bvids = []

for item in data["data"]["system_notify_list"]:
    if "下线" in item["content"] or "处理" in item["content"]:
        bvid = item["content"].split("【")[1].split("】")[0]
        bvids.append(bvid)

print(bvids)
with open(bvid_file, 'w', encoding='utf-8') as file:
    for bvid in bvids:
        file.write(f'{bvid}\n')