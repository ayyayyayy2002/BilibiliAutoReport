import subprocess
import sys
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
########################################################################################################################
log_file = os.path.join(base_dir,'运行记录','错误记录.txt')
log_directory = os.path.join(base_dir, '运行记录')
os.makedirs(log_directory, exist_ok=True)
skip = True




while True:
    if not skip:
        while True:
            print('启动Getuid.py')
            getuid_process = subprocess.Popen([sys.executable, 'GetUid.py'])
            getuid_process.wait()  # 等待 Getuid.py 结束


            if getuid_process.returncode == 0:# 检查 Getuid.py 的退出状态
                print("Getuid.py 正常退出，正在启动 Report.py...")
                break  # 退出此循环，开始启动 Report.py
            else:
                error_message = f"Getuid.py 出现错误，返回码: {getuid_process.returncode}，正在重新运行 Getuid.py..."
                print(error_message)
        print('启动SpaceAndDynamic.py')
        SpaceAndDynamic_process = subprocess.Popen([sys.executable, 'SpaceAndDynamic.py'])


    else:
        print('首次运行跳过')
        skip = False
    while True:
        #report_process.wait()  # 不等待 SpaceAndDynamic.py 结束
        print('启动Report.py')
        report_process = subprocess.Popen([sys.executable, 'Report.py'])
        report_process.wait()  # 等待 Report.py 结束


        if report_process.returncode == 0: # 检查 Report.py 的退出状态
            print("Report.py 正常退出，正在重新启动 Getuid.py...")
            break  # 退出此循环，重新开始下一轮
        else:
            error_message = f"Report.py 出现错误，返回码: {report_process.returncode}，正在重新运行 Report.py..."
            print(error_message)