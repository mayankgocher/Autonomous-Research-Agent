#!/bin/bash

echo "Initialization of Ollama models for Autonomous Research Agent"
echo ""

echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null
then
    echo "Ollama could not be found. Please install it from https://ollama.com/"
    exit 1
fi

echo ""
echo "Pulling Qwen2.5:7b model (Default LLM)..."
ollama pull qwen2.5:7b

echo ""
echo "Model downloaded successfully. You can now start the application!"
