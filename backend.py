from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uvicorn
from pynvml import *

app = FastAPI()

# --- GPU Initialization ---
try:
    nvmlInit()
    # Handle for your RTX 3090 (Device 0)
    gpu_handle = nvmlDeviceGetHandleByIndex(0)
except Exception as e:
    print(f"GPU Initialization Failed: {e}")
    gpu_handle = None

class ChatRequest(BaseModel):
    prompt: str
    model: str = "deepseek-r1:32b"

@app.get("/gpu-stats")
async def get_gpu_stats():
    if not gpu_handle:
        return {"error": "GPU not detected"}
    
    info = nvmlDeviceGetMemoryInfo(gpu_handle)
    used = info.used / 1024**3
    total = info.total / 1024**3
    return {
        "used_gb": round(used, 2),
        "total_gb": round(total, 2),
        "free_gb": round(total - used, 2),
        "percentage": round((used / total) * 100, 1)
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    ollama_url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "stream": False
    }
    try:
        response = requests.post(ollama_url, json=payload, timeout=120)
        return response.json()
    except Exception as e:
        return {"response": f"Ollama Error: {str(e)}"}

if __name__ == "__main__":
    # MUST bind to 127.0.0.1 so the SSH tunnel can find it
    uvicorn.run(app, host="127.0.0.1", port=8000)