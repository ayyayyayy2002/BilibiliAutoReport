# BilibiliAutoReport  
## 使用[关键词](https://raw.githubusercontent.com/ayyayyayy2002/BilibiliAutoReport/refs/heads/main/%E9%99%84%E5%8A%A0%E6%96%87%E4%BB%B6/keywords.txt)搜索视频，举报作者的头像、签名、昵称、视频和动态  
## 使用条款与免责声明
本项目是开源的，遵循以下条款和条件。请在使用本项目之前仔细阅读。
1. **无保证**：本项目以“现状”提供，不附带任何形式的明示或暗示保证，包括但不限于对适销性、特定用途适用性及不侵权的保证。  
2. **风险自担**：使用本项目过程中可能出现的问题或损失，使用者需自行承担所有风险。我们不对因使用本项目而引起的任何直接、间接、惩罚性或偶然的损害负责。此项目供仅学习使用，切勿用于违规操作。请于下载后24小时内删除。
3. **维护责任**：开发者不承诺对本项目的更新、维护或支持，用户应自行评估项目的适用性。

## 写在前面————引用信息🤓☝️ 
1，此项目的灵感来源于这个油猴脚本：[bilibili批量举报【高危脚本】-油猴中文网](https://bbs.tampermonkey.net.cn/thread-5222-2-1.html)  
2，项目中用Selenium完成人机验证的代码来自于[MgArcher/Text_select_captcha: 实现文字点选、选字、选择、点触验证码识别，基于pytorch训练](https://github.com/MgArcher/Text_select_captcha/)，感谢大佬  
3，项目中纯Python破解人机验证的代码来自于[ravizhan/geetest-v3-click-crack: 极验三代文字点选验证码破解 纯Python实现](https://github.com/ravizhan/geetest-v3-click-crack)，感谢大佬   
4，油猴举报脚本在[这里](https://greasyfork.org/zh-CN/scripts/497079-bilibili%E7%A8%BF%E4%BB%B6%E6%89%B9%E9%87%8F%E4%B8%BE%E6%8A%A5)  
5，网络请求代码全部来自此网站的转换：[Convert curl commands to code](https://curlconverter.com/)  
6，此项目的全部代码由[ChatGPT3.5Turbo](https://platform.openai.com/docs/models/gpt-3-5#gpt-3-5-turbo)完成  

## 此仓库可能包含多个分支，请注意识别🛑
1，**Python+Selenium**分支：默认分支，**纯Python，浏览器过人机验证**，关键词搜索+稍后再看+黑白名单  
2，**Python+Selenium+JavaScript**分支：**Python结构，JavaScript举报，浏览器过人机验证**，关键词搜索+稍后再看+黑白名单  
3，**Python**分支：**纯Python实现，破解人机验证**，稍后再看+黑白名单,不需要浏览器，但是运行一段时间后会被风控  


## 使用方法（仅限Windows，可能需要下载PyCharm）🐍 
1，前往[这里](https://github.com/ayyayyayy2002/BilibiliAutoReport/archive/refs/heads/main.zip)下载项目并解压     
2，搜索下载Chromium和对应版本的驱动，并解压后重命名为“chrome-win”和“chromedriver.exe”，移动到“附加文件”  
2，下载安装[Python3.10](https://www.python.org/downloads/release/python-3100/)  
  
<details>
<summary>不使用Pycharm： </summary>
  
 - 3a.1，进入解压后的文件夹，双击打开“启动脚本”，双击运行“安装依赖.bat”，等待运行结束   
 - 3a.2，双击运行“AAA.bat”，在打开的浏览器里登陆账号，然后关闭窗口  
 - 3a.3，双击运行”Start.bat“  
</details>
  
<details>
<summary>使用Pycharm：</summary>  
  
 - 3b.1，下载安装[PyCharm](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC)  
 - 3b.1，按照[教程](https://www.bing.com/search?q=PyCharm%E5%AE%89%E8%A3%85%E6%B1%89%E5%8C%96%E6%95%99%E7%A8%8B)安装和汉化PyCharm  
 - 3b.3，在Pycharm中打开源码文件夹，在软件的左侧是项目文件，右键点击指定文件，选择“运行”    
 - 3b.4，先运行AAA，在打开的浏览器中登录，等待程序自动结束。
 - 3b.5，关闭浏览器，点击左边向下三角，切换并运行Getuid，并查看是否成功启动浏览器  
 - 3b.6，双击红色停止按钮，彻底停止脚本，切换至Start，点击绿色三角 
</details>  
4，脚本已运行  

## Linux系统使用方法（未尝试）❗
本项目理论上支持Linux系统，仅需要修改浏览器和驱动可执行文件名称即可。  
值得注意的是，Chrome和Chromium浏览器官方不支持某些架构。如：ARM32Linux的玩客云盒子，此类设备只能运行针对动态和主页的举报，无法完成视频的举报。  
另外B站无法通过导入浏览器cookie登录，Linux设备大多不提供图形界面。程序会尝试在终端用字符显示登陆二维码，如图所示：  
<img src="https://raw.githubusercontent.com/ayyayyayy2002/BilibiliAutoReport/refs/heads/Python+Selenium/%E9%99%84%E5%8A%A0%E6%96%87%E4%BB%B6/%E5%9B%BE%E7%89%87/1.png" alt="如图所示" width="600" />  

    

## 程序逻辑🧠   
1，Start.是守护进程，负责启动其他三个程序，运行后会启动Getuid  
2，Getuid加载关键词列表、黑名单和白名单，请求获取“稍后再看”列表，用关键词搜索得到原始列表。原始列表+白名单=稍后再看-黑名单后，去重，写入文件uid.txt  
3，处理完uid会自动启动Report和SpaceAndDynamic进行举报，如果中途出错将重新启动Report，如果Report正常退出则重新运行Getuid获得新列表 
4，需要人机验证时会自动调用Capcha完成验证并更新Cookie  
5，举报每个UID的所有动态，主页信息和包括合集在内的前200条视频        

## 目前问题😒  
1，采用关键词搜索寻找目标的方法容易误杀，未来可能会采取更好的方法来获取目标  
2，孪生网络模型识别成功率有待加强，后续会进行训练  



 

