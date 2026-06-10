@echo off
title AI Tool Curator - LLM Server
cd /d "%~dp0"

echo Starting llama-server with Gemma 4 E4B...
echo Model: google_gemma-4-E4B-it-Q4_K_M.gguf
echo Context: 8192 tokens
echo Port: 8080
echo.

llama.cpp\build\bin\llama-server.exe ^
    -m llama.cpp\models\google_gemma-4-E4B-it-Q4_K_M.gguf ^
    --chat-template gemma ^
    --host 127.0.0.1 ^
    --port 8080 ^
    -c 8192 ^
    --temp 0.3 ^
    --jinja

pause
