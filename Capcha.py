from dotenv import load_dotenv
import requests
import re
import os
import time
from crack import Crack
from model import Model


def capcha(aid, json=None):
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
        'attach':'',
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
    print(response.text)
    data = json.loads(response.text)
    if 'data' in data and 'geetest' in data['data']:
        gt = data['data']['geetest']['gt']
        challenge = data['data']['geetest']['challenge']
        token = data['data']['token']
    else:
        gt, challenge, token = '', '', ''
        print(response.text)

    print(gt, challenge)
    crack = Crack(gt, challenge)
    crack.gettype()
    crack.get_c_s()
    time.sleep(0.5)
    crack.ajax()
    model = Model()
    for retry in range(6):
        tt = time.time()
        pic_content = crack.get_pic(retry)
        print(time.time() - tt)

        ttt = tt = time.time()
        small_img, big_img = model.detect(pic_content)
        print(
            f"检测到小图: {len(small_img.keys())}个,大图: {len(big_img)} 个,用时: {time.time() - tt}s"
        )
        tt = time.time()
        result_list = model.siamese(small_img, big_img)
        print(f"文字配对完成,用时: {time.time() - tt}")
        point_list = []
        # print(result_list)
        for i in result_list:
            left = str(round((i[0] + 30) / 333 * 10000))
            top = str(round((i[1] + 30) / 333 * 10000))
            point_list.append(f"{left}_{top}")
        wait_time = 2.0 - (time.time() - ttt)
        time.sleep(wait_time)
        tt = time.time()
        data = json.loads(crack.verify(point_list))
        print(data)
        print(time.time() - tt)
        if data["data"]["result"] == "success":
            break

    # 检查 'data' 中是否包含 'validate' 键
    if isinstance(data, dict) and 'data' in data:

        validate = data['data']['validate']
        print("validate 存在:", validate)
    else:
        print("validate 不存在")
        validate = ''

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
