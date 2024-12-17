import random

from dotenv import load_dotenv, set_key
from datetime import datetime
from Capcha import capcha
import requests
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
uids = set()
load_dotenv(dotenv_path=env_file)
UA = os.getenv('UA')
N = os.getenv('N')
COOKIE1 = os.getenv('COOKIE1')
########################################################################################################################

tids_with_weights = {
    '2':1,  # 违法违禁
    '5':1,  # 赌博诈骗
    '10025':1,  # 违法信息外链
    '10014':1,#涉政谣言
    '10015':1,#涉社会事件谣言
    '10017':1,#虚假不实信息
    '10018':1,#违规推广
    '52':1,#转载/自制错误
    '10019':1,#其他不规范行为
    '7':1,#人身攻击
    '9':1,#引战
    '3':1,#色情低俗
    '10020':1,#危险行为
    '10021':1,#观感不适
    '6':1,#血腥暴力
    '10000':1,#青少年不良信息
    '10022':1,#其他
}
tids = list(tids_with_weights.keys())
weights = list(tids_with_weights.values())

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

    else:
        print(f"UID: {uid} NAME: {name}")
        aid_log_file = os.path.join(base_dir, '运行记录', 'UID记录', f'{uid}.txt')
        with open(aid_log_file, 'w', encoding='utf-8') as file:
            file.write(f"UID: {uid} NAME: {name}\n")

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

    print(f'合集视频个数:{len(aids)},合集标题个数:{len(titles)},合集封面个数:{len(pics)}')
    aid_log_file = os.path.join(base_dir, '运行记录', 'UID记录', f'{uid}.txt')
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"合集视频个数:{len(aids)},合集标题个数:{len(titles)},合集图片个数:{len(pics)}\n")

    search_url = f'https://api.bilibili.com/x/series/recArchivesByKeywords?mid={uid}&keywords=&ps=0'
    headers = {'cookie': COOKIE1, 'user-agent': UA}
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(3, 3))
    data = response.json()
    for archive in data['data']['archives']:
        aids.append(archive['aid'])
        titles.append(archive['title'])
        pics.append(archive['pic'])

    print(f'全部视频个数:{len(aids)},全部标题个数:{len(titles)},普全部封面个数:{len(pics)}')
    aid_log_file = os.path.join(base_dir, '运行记录', 'UID记录', f'{uid}.txt')
    with open(aid_log_file, 'a', encoding='utf-8') as file:
        file.write(f"普通视频个数:{len(aids)},普通标题个数:{len(titles)},普通图片个数:{len(pics)}\n")

    for i in range(1, int(N) + 1):
        tid = random.choices(tids, weights=weights, k=1)[0]
        print(f'\n账号{i}  https://space.bilibili.com/{uid}\n')
        reportcount = 0
        cookie_name = f'COOKIE{i}'
        COOKIE = os.getenv(cookie_name)
        CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)

        for aid, title, pic in zip(aids, titles, pics):

            reportcount += 1
            time.sleep(2.3)
            headers = {'cookie': COOKIE, 'user-agent': UA}
            data = {
                'aid': aid,
                'attach': pic,
                'block_author': 'false',
                'csrf': CSRF,
                'desc': f'违规行为：在视频标题及评论中支持“台独”行为，并辱骂讽刺政府和领导人。视频标题{title}违规推广色情游戏，视频封面是色情游戏截图。在置顶动态和评论发布加密链接传播色情内容，严重违反刑法第三百六十四条【传播淫秽物品罪】 传播淫秽的书刊、影片、音像、图片或者其他淫秽物品。诉求：下架此视频并处罚发送此视频的账号',
                'tid': tid
            }
            response = requests.post('https://api.bilibili.com/x/web-interface/appeal/v2/submit', headers=headers,
                                     data=data, proxies=proxies, timeout=(3, 3))
            print(f'账号{i}视频{reportcount:03}:{response.text}')
            if "62009" in response.text or reportcount >= 200:
                break
            elif "-352" in response.text:
                COOKIE = capcha(aid, i)
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

            aid_log_file = os.path.join(base_dir, '运行记录', 'UID记录', f'{uid}.txt')
            with open(aid_log_file, 'a', encoding='utf-8') as file:
                file.write(f'{aid},{tid}\n')

with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}结束\n')
