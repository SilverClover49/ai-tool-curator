@echo off
title AI Tool Curator - LLM Server
cd /d "%~dp0"

echo Starting llama-server with Gemma 4 12B QAT + MTP...
echo Model: gemma-4-12B-it-qat-UD-Q4_K_XL.gguf
echo MTP: mtp-gemma-4-12B-it.gguf
echo Context: 8192 tokens
echo Port: 8080
echo.

llama.cpp\build\bin\llama-server.exe ^
    -m llama.cpp\models\gemma-4-12B-it-qat-UD-Q4_K_XL.gguf ^
    --model-draft llama.cpp\models\mtp-gemma-4-12B-it.gguf ^
    --spec-type draft-mtp ^
    --spec-draft-n-max 3 ^
    --chat-template gemma ^
    --host 127.0.0.1 ^
    --port 8080 ^
    -c 8192 ^
    --temp 0.3 ^
    --jinja

pause
