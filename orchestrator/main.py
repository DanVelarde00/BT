from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

LM_API_URL = os.getenv("LM_API_URL", "http://host.docker.internal:11434")

MODEL_NAME = "qwen3-8b"

print(f"Using LM API URL: {LM_API_URL}")
@app.post("/orchestrate")
async def orchestrate(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    
    lm_payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{LM_API_URL}/v1/chat/completions", json=lm_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "details": response.text if 'response' in locals() else "no response"}
