import json
import bili_ticket_gt_python
from dotenv import load_dotenv
import requests
import re
import os
import time
from crack import Crack
from model import Model





def capcha(aid):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(base_dir, '附加文件', '.env')
    proxies = {'http': None, 'https': None}
    load_dotenv(dotenv_path=env_file)
    COOKIE = os.getenv('COOKIE')
    UA = os.getenv('UA')
    CSRF = re.search(r'bili_jct=([^;]*)', COOKIE).group(1)

    headers = {'cookie': COOKIE, 'user-agent': UA}
    data = {
        'aid': aid,
        'attach': '',
        'block_author': 'false',
        'csrf': CSRF,
        'desc': '理由',
        'tid': '10014',
    }
    response = requests.post('https://api.bilibili.com/x/web-interface/appeal/v2/submit', headers=headers,
                             data=data, proxies=proxies)
    if response.headers.get('X-Bili-Gaia-Vvoucher'):
        v_voucher = response.headers.get('X-Bili-Gaia-Vvoucher')
    else:
        v_voucher = ""
        print(response.headers)

    headers = {'cookie': COOKIE, 'user-agent': UA}
    data = {
        'csrf': CSRF,
        'v_voucher': v_voucher,
    }
    response = requests.post('https://api.bilibili.com/x/gaia-vgate/v1/register', headers=headers, data=data,
                             proxies=proxies)
    data = json.loads(response.text)
    if 'data' in data and 'geetest' in data['data']:
        gt = data['data']['geetest']['gt']
        challenge = data['data']['geetest']['challenge']
        token = data['data']['token']
    else:
        gt, challenge, token = '', '', ''
        print(response.text)

    print(gt, challenge)
    click = bili_ticket_gt_python.ClickPy()
    try:

        validate = click.simple_match_retry(gt, challenge)
        print(validate)
    except Exception as e:
        print("识别失败")
        print(e)

    headers = {'cookie': COOKIE, 'user-agent': UA}
    data = {
        'challenge': challenge,
        'csrf': CSRF,
        'seccode': f'{validate}|jordan',
        'token': token,
        'validate': validate,
    }
    print(data)
    response = requests.post('https://api.bilibili.com/x/gaia-vgate/v1/validate', headers=headers,
                             data=data, proxies=proxies)
    print(response.text)

    COOKIE += f'; x-bili-gaia-vtoken={token}'
    headers = {'cookie': COOKIE, 'user-agent': UA}
    params = {
        'gaia_vtoken': token,
    }
    data = {
        'aid': aid,
        'attach': '',
        'block_author': 'false',
        'csrf': CSRF,
        'desc': '理由',
        'tid': '2',
    }
    response = requests.post(
        'https://api.bilibili.com/x/web-interface/appeal/v2/submit',
        params=params,
        headers=headers,
        data=data,
        proxies=proxies
    )

    print(response.text)

    return COOKIE


