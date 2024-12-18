from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
uids = set()

proxies = {'http': None, 'https': None}
base_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(base_dir,  'User Data')
chrome_binary_path = os.path.join(base_dir,  'chrome-win', 'chrome.exe')
chrome_driver_path = os.path.join(base_dir,  'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'--user-data-dir={user_data_dir}')
options.binary_location = chrome_binary_path
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument("--disable-gpu")
options.add_argument("--disable-sync")
options.add_argument("disable-cache")  # 禁用缓存
options.add_argument('log-level=3')
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # 启动 Chrome 浏览器
driver.set_window_size(1000, 700)  # 设置浏览器窗口大小（宽度, 高度）
uid_file = os.path.join(base_dir, 'uid.txt')

try:
    with open(uid_file, 'r', encoding='utf-8') as file:  # 以读取模式打开文件
        for line in file:
            line = line.strip()  # 去掉行首尾的空白字符
            uids.add(line)
except Exception as e:
    print(f"无法读取UID文件: {e}")
    exit(0)

for uid in uids:
    driver.get(f"https://space.bilibili.com/{uid}/dynamic")
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
    input("请按回车键继续...")




