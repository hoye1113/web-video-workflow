@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem 这台机器上要用到的东西都在非默认位置，先把 PATH 补齐
set "PYTHONUTF8=1"
set "PATH=%PATH%;%USERPROFILE%\.local\bin;%LOCALAPPDATA%\Microsoft\WinGet\Links;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts"

where python >nul 2>nul || (echo [x] 找不到 python，先装 Python 3.12 && pause && exit /b 1)
where ffmpeg >nul 2>nul || (echo [!] 找不到 ffmpeg，出片和拼接会失败)
where uv     >nul 2>nul || (echo [!] 找不到 uv，渲染会失败)

echo.
echo   video-factory   http://127.0.0.1:8777
echo   （关掉这个窗口就是停服务）
echo.

rem 等 3 秒再开浏览器，免得服务还没起来
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:8777/"

python app\server.py --port 8777
