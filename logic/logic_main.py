# logic/main.py
from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

LOGIC_URL = os.getenv("LM_API_URL", "http://host.docker.internal:1234")
MODEL_NAME = os.getenv("MODEL_NAME", "phi-4")

@app.post("/route")
async def route(req: Request):
    data = await req.json()
    instruction = data.get("instruction", "")

    prompt = f"""
You are the decision-making core of a modular AI system.
Given this user instruction: \"{instruction}\"
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
        response = requests.post(f"{LOGIC_URL}/v1/chat/completions", json=payload)
        response.raise_for_status()
        model_output = response.json()
        raw_text = model_output["choices"][0]["message"]["content"]

        # Extract JSON from within ```json ... ``` or similar blocks
        import json, re
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            routing_plan = json.loads(match.group(0))
            return routing_plan
        else:
            return {"error": "No valid JSON found in model output", "raw": raw_text}

    except Exception as e:
        return {
            "error": str(e),
            "details": response.text if 'response' in locals() else "No response from model"
        }

