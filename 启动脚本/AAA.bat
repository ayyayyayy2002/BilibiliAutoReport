=@echo off
chcp 65001
setlocal
pushd ..
call venv\Scripts\activate.bat
python AAA.py
popd
pause
endlocal
