@echo off
title AI Tool Curator - Pipeline
cd /d "%~dp0"

echo ========================================
echo  AI Tool Curator - Run Pipeline
echo ========================================
echo.
echo Make sure start-server.cmd is running in another window!
echo Place your Google Takeout files in data/raw\ then press any key.
echo.
pause

python -m src.pipeline

echo.
echo Done! Open the 'vault' folder in Obsidian.
pause
