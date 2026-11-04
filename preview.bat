@echo off
cd /d "%~dp0"
echo Building the site and opening a preview (drafts included). Close this window to stop.
python build.py --serve
pause
