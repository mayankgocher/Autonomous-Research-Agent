@echo off
echo Initialization of Ollama models for Autonomous Research Agent
echo.

echo Make sure Ollama is installed and running on your system.
echo Checking for Ollama...
ollama --version
IF %ERRORLEVEL% NEQ 0 (
    echo Ollama is not installed or not in PATH. Please install it from https://ollama.com/
    pause
    exit /b
)

echo.
echo Pulling Qwen2.5:7b model (Default LLM)...
ollama pull qwen2.5:7b

echo.
echo Model downloaded successfully. You can now start the application!
pause
