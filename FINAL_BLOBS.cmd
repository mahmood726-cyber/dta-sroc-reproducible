@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
python recut_integrity.py --verify
if errorlevel 1 exit /b 1
python fix_app_sources.py --upstream "..\allmeta"
if errorlevel 1 exit /b 1
exit /b 0
