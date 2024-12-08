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

    reportcount = 0
    headers = {'cookie': COOKIE, 'user-agent': UA}
    search_url = f'https://api.bilibili.com/x/polymer/space/seasons_series_list?mid={uid}&page_num=1&page_size=5'
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    if data.get('data', {}).get('items_lists', {}).get('seasons_list', []):
        season_ids = [season['meta']['season_id'] for season in data.get('data', {}).get('items_lists', {}).get('seasons_list', [])]

        for season_id in season_ids:
            search_url = f'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid={uid}&sort_reverse=false&season_id={season_id}&page_num=1&page_size=30'
            headers = {'cookie': COOKIE, 'user-agent': UA}
            response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
            data = response.json()
            if 'data' in data and 'archives' in data['data']:
                for archive in data['data']['archives']:
                    aids.append(archive['aid'])  # 添加 aid 到集合
                    titles.append(archive['title'])  # 添加 title 到列表
                    pics.append(archive['pic'])  # 添加 pic 到列表

    search_url = f'https://api.bilibili.com/x/series/recArchivesByKeywords?mid={uid}&keywords=&ps=0'
    headers = {'cookie': COOKIE, 'user-agent': UA}
    response = requests.get(search_url, headers=headers, proxies=proxies, timeout=(5, 10))
    data = response.json()
    for archive in data['data']['archives']:
        aids.append(archive['aid'])
        titles.append(archive['title'])
        pics.append(archive['pic'])



    if aids and aids[0]:
        headers = {'cookie': COOKIE, 'user-agent': UA}
        data = {
            'rid': aids[0],
            'type': '2',
            'add_media_ids': MEDIAID,
            'del_media_ids': '',
            'platform': 'web',
            'eab_x': '2',
            'ramval': '0',
            'ga': '1',
            'gaia_source': 'web_normal',
            'csrf': CSRF,}
        response = requests.post('https://api.bilibili.com/x/v3/fav/resource/deal',  headers=headers, data=data,proxies=proxies)
        print(f'收藏{aids[0]}:{response.text}')
        print(f'\nhttps://space.bilibili.com/{uid}\n')


        aid_log_file = os.path.join(base_dir, '运行记录','UID记录', f'{uid}.txt')
        with open(aid_log_file, 'w', encoding='utf-8') as file:
            for aid in aids:
                file.write(f'{aid}\n')




    for aid, title, pic in zip(aids, titles, pics):
        reportcount += 1
        time.sleep(2.3)
        headers = {'cookie': COOKIE, 'user-agent': UA}
        data = {
            'aid': aid,
            'attach': pic,
            'block_author': 'false',
            'csrf': CSRF,
            'desc': f'视频标题{title}、视频封面以及视频内容违规，推广以原神、碧蓝档案等二次元游戏人物为主角的色情视频，侮辱国家领导人，宣扬台独反华内容。审核结果：下架此视频并永久封禁该账号',
            'tid': '10019'
        }
        response = requests.post('https://api.bilibili.com/x/web-interface/appeal/v2/submit', headers=headers,data=data, proxies=proxies)
        print(f'视频{reportcount:03}:{response.text}')
        if "62009" in response.text or reportcount >= 200:
            break
        elif "-352" in response.text:
            COOKIE = capcha(aid)
            os.environ['COOKIE'] = COOKIE



with open(log_file, 'a', encoding='utf-8') as log:
    timestamp = datetime.now().strftime('[%Y-%m-%d %H-%M-%S]')
    log.write(f'{timestamp}结束\n')









