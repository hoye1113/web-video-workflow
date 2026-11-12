@echo off
cd /d "%~dp0"
node engine\tools\render.mjs --skip-subs --fps 30 %*
if errorlevel 1 pause
