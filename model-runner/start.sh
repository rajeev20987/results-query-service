#!/bin/sh

# Start Ollama server in background
ollama serve &

# Wait for server to be ready
echo "Waiting for Ollama to start..."
sleep 5

# Pull the model (if not already present)
echo "Pulling model: qwen2.5:3b"
ollama pull qwen2.5:3b

# Keep container running by waiting on background process
wait