@echo off
chcp 65001
cd ../
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python AAA.py
pause
