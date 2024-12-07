=@echo off
chcp 65001
setlocal
pushd ..
call venv\Scripts\activate.bat
python Report.py
popd
pause
endlocal
