This repository contains a full-stack, local LLM implementation. It is architected for NVIDIA RTX 3090 (24GB VRAM) hardware, utilizing a decoupled backend for high-performance inference and a Streamlit frontend with live GPU monitoring.

# Prerequisites

Linux (Ubuntu/Debian) with NVIDIA Drivers.

Ollama installed: curl -fsSL https://ollama.com/install.sh | sh.

Python 3.10+

# Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate

# Install core dependencies

pip install streamlit fastapi uvicorn requests nvidia-ml-py

Model Preparation

Run this command in your terminal to download the 32B reasoning model:

ollama run deepseek-r1:32b

# Execution Instructions

To run the full stack on a remote machine (like Vast.ai) with a single SSH session:

Start Ollama: ollama serve (Run in Pane 0).

Launch Backend: python backend.py (Run in Pane 1).

Launch Frontend: streamlit run frontend.py --server.address 127.0.0.1 --server.port 8501 (Run in Pane 2).

# Accessing Locally
On your laptop terminal, run:

ssh -L 8501:localhost:8501 -L 8000:localhost:8000 -p [PORT] root@[IP]
Visit http://localhost:8501 to start chatting.