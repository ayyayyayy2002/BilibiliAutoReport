=@echo off
chcp 65001
setlocal
pushd ..
call venv\Scripts\activate.bat
python Start.py
popd
pause
endlocal
