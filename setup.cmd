@echo off
title AI Tool Curator - Setup
cd /d "%~dp0"

echo ========================================
echo  AI Tool Curator - One-Time Setup
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
echo.

echo [2/4] Checking llama.cpp build...
if exist "llama.cpp\build\bin\llama-server.exe" (
    echo   llama.cpp already built!
) else (
    echo   llama.cpp not found. Building...
    echo   This requires MSYS2 UCRT64 with cmake and ninja.
    echo.
    set CC=C:\msys64\ucrt64\bin\gcc.exe
    set CXX=C:\msys64\ucrt64\bin\g++.exe
    cd llama.cpp
    cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=OFF -DCMAKE_CXX_FLAGS="-DWINVER=0x0A00 -D_WIN32_WINNT=0x0A00"
    cmake --build build --config Release
    cd ..
)
echo.

echo [3/4] Checking model...
if exist "llama.cpp\models\google_gemma-4-E4B-it-Q4_K_M.gguf" (
    echo   Gemma 4 E4B model found!
) else (
    echo   Downloading Gemma 4 E4B Q4_K_M (~5.4 GB)...
    hf download bartowski/google_gemma-4-E4B-it-GGUF --include "google_gemma-4-E4B-it-Q4_K_M.gguf" --local-dir llama.cpp\models
)
echo.

echo [4/4] Setup complete!
echo.
echo To use:
echo   1. Run start-server.cmd (starts LLM server)
echo   2. Place Google Takeout files in data/raw\
echo   3. Run run.cmd (runs the pipeline)
echo   4. Open vault/ in Obsidian
echo.
pause
