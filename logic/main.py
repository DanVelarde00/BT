# logic/main.py
from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

LM_API_URL = os.getenv("LM_API_URL", "http://host.docker.internal:1234")
MODEL_NAME = os.getenv("MODEL_NAME", "phi-4")

@app.post("/route")
async def route(req: Request):
    data = await req.json()
    instruction = data.get("instruction", "")

    prompt = f"""
You are the decision-making core of a modular AI system.
Given this user instruction: "{instruction}"
Return a JSON object identifying which agent should handle the task first, and optionally any follow-up agents.

Respond ONLY in this format:
{{"agent": "planner", "next": ["coder", "critic"]}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(f"{LM_API_URL}/v1/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "details": response.text if 'response' in locals() else "No response from logic agent"}
