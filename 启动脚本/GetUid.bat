=@echo off
chcp 65001
setlocal
pushd ..
call venv\Scripts\activate.bat
python GetUid.py
popd
pause
endlocal
