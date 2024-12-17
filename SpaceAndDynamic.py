import os
import re
import requests
from dotenv import load_dotenv

proxies = {'http': None, 'https': None}
base_dir = os.path.dirname(os.path.abspath(__file__))

uid_file = os.path.join(base_dir, '附加文件', 'uid.txt')

env_file = os.path.join(base_dir, '附加文件', '.env')
load_dotenv(dotenv_path=env_file)
UA = os.getenv('UA')
N = os.getenv('N')
uids = set()


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
    print(uid)

    for i in range(1, int(N) + 1):
        reportcount = 0
        cookie_name = f'COOKIE{i}'
        COOKIE = os.getenv(cookie_name)
        CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)



        headers = {'cookie': COOKIE, 'user-agent': UA}
        data = {
            'mid': uid,
            'reason': '1,2,3',
            'reason_v2': '3',
            'csrf': CSRF, }
        response = requests.post('https://space.bilibili.com/ajax/report/add', headers=headers, data=data, proxies=proxies)
        print(response.text)

        offset = ''
        csrf = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)

        while True:
            headers = {'cookie': COOKIE, 'user-agent': UA}
            params = {
                'host_mid': uid,
                'offset': offset,}
            response = requests.get('https://api.bilibili.com/x/polymer/web-dynamic/v1/opus/feed/space',params=params,headers=headers,proxies = proxies,timeout=(3,3))
           #response = requests.get('https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all',params=params,headers=headers,proxies = proxies,timeout=(3,3))
            data = response.json()
            if 'data' in data:
                opus_ids = [item['opus_id'] for item in data['data']['items']]
                offset = data['data']['offset']
                has_more = data['data']['has_more']
            else:
                print("JSON 对象中不包含 'data' 字段")
                print(response.text)
                offset = ''
                has_more = ''
                id_strs = []


            # 打印结果
            #print(has_more)
            print(opus_ids)
            #print(offset)
            for opus_id in opus_ids:
                reportcount += 1
                headers = {'cookie': COOKIE, 'user-agent': UA}
                params = {'csrf': csrf,}
                json_data = {
                    'accused_uid': int(uid),
                    'dynamic_id': opus_id,
                    'reason_type': 0,
                    'reason_desc': '违规行为：在标题及评论中支持“台独”行为，并辱骂讽刺政府和领导人。诉求：删除此动态并处罚发送此视频的账号',}
                response = requests.post('https://api.bilibili.com/x/dynamic/feed/dynamic_report/add',params=params,headers=headers,json=json_data,proxies=proxies,timeout=(3,3))
                print(f'账号{i}动态{reportcount:03}:{response.text}')
            opus_ids.clear()
            if not has_more:
                break










