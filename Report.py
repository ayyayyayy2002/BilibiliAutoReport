from dotenv import load_dotenv
from datetime import datetime
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


            COOKIE = capcha(aid)
            os.environ['COOKIE'] = COOKIE



with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}结束\n')









