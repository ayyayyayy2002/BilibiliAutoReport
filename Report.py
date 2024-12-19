from dotenv import load_dotenv, set_key
from datetime import datetime
from Capcha import capcha
from AVtoBV import enc
import subprocess
import argparse
import requests
import random
import time
import re
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
uid_file = os.path.join(base_dir, '附加文件', 'uid.txt')
list_file = os.path.join(base_dir, '附加文件', 'list')
log_file = os.path.join(base_dir, '运行记录', '循环记录.txt')
env_file = os.path.join(base_dir, '附加文件', '.env')
proxies = {'http': None, 'https': None}
uids = []
load_dotenv(dotenv_path=env_file)
UA = os.getenv('UA')
N = os.getenv('N')
COOKIE1 = os.getenv('COOKIE1')
########################################################################################################################

tids_with_weights = {
    '2':1,  # 违法违禁
    '5':1,  # 赌博诈骗
    '10025':1,  # 违法信息外链
    '10014':3,#涉政谣言
    '10015':4,#涉社会事件谣言
    '10017':1,#虚假不实信息
    '10018':6,#违规推广
    '52':4,#转载/自制错误
    '10019':2,#其他不规范行为
    '7':1,#人身攻击
    '9':1,#引战
    '3':1,#色情低俗
    '10020':2,#危险行为
    '10021':1,#观感不适
    '6':1,#血腥暴力
    '10000':1,#青少年不良信息
    '10022':1,#其他
}
tids = list(tids_with_weights.keys())
weights = list(tids_with_weights.values())





# 创建ArgumentParser对象
parser = argparse.ArgumentParser()
parser.add_argument('--git', default=False, action='store_true', help='Enable git')
args = parser.parse_args()

# 获取git参数值
git = args.git

print(f'Git is enabled: {git}')












try:
    with open(uid_file, 'r', encoding='utf-8') as file:  # 以读取模式打开文件
        for line in file:
            line = line.strip()  # 去掉行首尾的空白字符
            if line.isdigit():
                uids.append(line)
except Exception as e:
    print(f"无法读取UID文件: {e}")
    exit(0)

if not uids:
    print("uid.txt 文件中没有可处理的UID，程序退出")
    exit(0)

for uid in uids:
    date = datetime.now().strftime('[%m-%d]')
    aid_log_file = os.path.join(base_dir, '运行记录', '处理记录', f'{date}{uid}.txt')
    headers = {'cookie': COOKIE1, 'user-agent': UA}
    search_url = f'https://api.bilibili.com/x/web-interface/card?mid={uid}'
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    name = data['data']['card']['name']
    if name == "账号已注销":
        print(f"UID: {uid} 账号已注销")
        try:
            with open(list_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(list_file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != uid:
                        f.write(line)
            print(f"删除已注销UID: {uid}")
        except Exception as e:
            print(f"删除已注销UID时发生错误: {e}")


    print(f"UID: {uid} NAME: {name} TIME: {datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')}")
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"UID: {uid} NAME: {name} TIME: {datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')}3\n")

    aids = []
    titles = []
    pics = []

    headers = {'cookie': COOKIE1, 'user-agent': UA}
    search_url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={uid}&type=video'
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    for item in data["data"]["items"]:
        # 检查当前 item 的 "text" 字段是否为 "动态视频"
        text = item["modules"]["module_dynamic"]["major"]["archive"]["badge"]["text"]
        if text == "动态视频":
            # 提取 aid, title, cover 并添加到对应的集合
            aids.append(item["modules"]["module_dynamic"]["major"]["archive"]["aid"])
            titles.append(item["modules"]["module_dynamic"]["major"]["archive"]["title"])
            pics.append(item["modules"]["module_dynamic"]["major"]["archive"]["cover"])
    count1 = len(aids)
    print(f'动态视频个数:{count1}')
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"动态视频个数:{count1},")




    headers = {'cookie': COOKIE1, 'user-agent': UA}
    search_url = f'https://api.bilibili.com/x/polymer/space/seasons_series_list?mid={uid}&page_num=1&page_size=5'
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    if data.get('data', {}).get('items_lists', {}).get('seasons_list', []):
        season_ids = [season['meta']['season_id'] for season in
                      data.get('data', {}).get('items_lists', {}).get('seasons_list', [])]

        for season_id in season_ids:
            search_url = f'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={uid}&sort_reverse=false&season_id={season_id}&page_num=1&page_size=30'
            headers = {'cookie': COOKIE1, 'user-agent': UA}
            response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(3, 3))
            data = response.json()
            if 'data' in data and 'archives' in data['data']:
                for archive in data['data']['archives']:
                    aids.append(archive['aid'])  # 添加 aid 到集合
                    titles.append(archive['title'])  # 添加 title 到列表
                    pics.append(archive['pic'])  # 添加 pic 到列表
    count2 = len(aids) - count1
    print(f'合集视频个数:{count2}')
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"合集视频个数:{count2},")




    search_url = f'https://api.bilibili.com/x/series/recArchivesByKeywords?mid={uid}&keywords=&ps=0'
    headers = {'cookie': COOKIE1, 'user-agent': UA}
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(3, 3))
    data = response.json()
    for archive in data['data']['archives']:
        aids.append(archive['aid'])
        titles.append(archive['title'])
        pics.append(archive['pic'])
    count3 = len(aids) - count2 - count1
    print(f'普通视频个数:{count3}')
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"普通视频个数:{count3}\n")




    for i in range(1, int(N) + 1):

        print(f'\n账号{i}  https://space.bilibili.com/{uid}\n')
        reportcount = 0
        cookie_name = f'COOKIE{i}'
        COOKIE = os.getenv(cookie_name)
        CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)

        for aid, title, pic in zip(aids, titles, pics):
            tid = random.choices(tids, weights=weights, k=1)[0]
            reportcount += 1
            time.sleep(2.3)
            headers = {'cookie': COOKIE, 'user-agent': UA}
            #print(headers)
            data = {
                'aid': aid,
                'attach': pic,
                'block_author': 'false',
                'csrf': CSRF,
                'desc': f'违规行为：在视频标题{title}及评论中支持“台独”行为，并辱骂讽刺政府和领导人。诉求：下架此视频并处罚发送此视频的账号',
                'tid': tid
            }
            response = requests.post('https://api.bilibili.com/x/web-interface/appeal/v2/submit', headers=headers,
                                     data=data, proxies=proxies, timeout=(3, 3))
            print(f'账号{i}视频{reportcount:03}:{response.text}')
            if "62009" in response.text or reportcount >= 200:
                break
            elif "-352" in response.text or "-351" in response.text:
                COOKIE = capcha(aid, i)
                os.environ[cookie_name] = COOKIE
                set_key(env_file, cookie_name, COOKIE)



            elif "412" in response.text:
                print('被风控，等待五分钟')
                time.sleep(60)
                print('还剩4分钟')
                time.sleep(60)
                print('还剩3分钟')
                time.sleep(60)
                print('还剩2分钟')
                time.sleep(60)
                print('还剩1分钟')
                time.sleep(60)

            with open(aid_log_file, 'a', encoding='utf-8') as file:
                file.write(f'{enc(int(aid))},{tid}，{title}\n')


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




    if git:
        try:
            subprocess.run('git config --system --unset credential.helper', timeout=20, shell=True)
            subprocess.run('git config --global http.proxy http://127.0.0.1:7890', timeout=20, shell=True)
            subprocess.run('git config --global https.proxy https://127.0.0.1:7890', timeout=20, shell=True)

            print('1')
            # subprocess.run('git config --system credential.helper manager', timeout=20, shell=True)
            print('2')
            subprocess.run('git pull --no-edit', timeout=20, shell=True)
            print('3')
            subprocess.run('git add .', timeout=20, shell=True)
            print('4')
            subprocess.run('git commit -m "txt"', timeout=20, shell=True)
            print('5')
            subprocess.run('git push', timeout=30, shell=True)
            print('6')

        except Exception as e:
            print(e)













with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}结束\n')
