from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

LM_API_URL = os.getenv("LM_API_URL", "http://host.docker.internal:11434")

MODEL_NAME = "qwen3-8b"
LOGIC_URL = os.getenv("LOGIC_URL", "http://logic:8005/route")
SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "orchestrator/prompt/system.txt")

AGENT_PORTS = {
    "planner": "8001",
    "coder": "8002",
    "critic": "8003",
    "memory": "8004"
}

def load_system_prompt():
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        base_prompt = f.read().strip()
    
    # Add decision protocol directive
    decision_directive = """
\nDecision Protocol for Delegation:
For every user prompt:
- If the prompt is conversational, respond directly as BT-7274. You may store relevant facts in the Memory subsystem, but do not delegate unless specified.
- If the prompt involves building, developing, analyzing, or planning a solution, delegate the task.
  - In this case, send the task to the Logic Protocol first. It will determine which subsystems (Planner, Coder, Critic, etc.) are required.
  - The Logic subsystem will report back the planned delegation structure.
  - You must then report the delegation plan clearly to the Pilot.
- Always include the line:
DELEGATE: <brief reason for delegation>
...only when actual delegation will be triggered.
"""

    return base_prompt + "\n\n" + decision_directive

SYSTEM_PROMPT = load_system_prompt()

def query_bt(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 32768
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{LM_API_URL}/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"BT encountered an error: {str(e)}"

@app.post("/orchestrate")
async def orchestrate(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")

    # Step 1: Ask BT whether to respond directly or delegate
    decision_response = query_bt(prompt)
# If not explicitly delegating, check for indirect signals
    if "DELEGATE:" not in decision_response:
        if any(word in decision_response.lower() for word in ["engaging", "deploying", "coder", "planner", "critic", "subsystem"]):
            decision_response += "\n\nDELEGATE: Detected multi-agent coordination. Delegating to Logic protocol."
        else:
            return {"response": decision_response.strip()}



    # Step 2: Otherwise delegate via logic
    try:
        logic_response = requests.post(LOGIC_URL, json={"instruction": prompt})
        logic_response.raise_for_status()
        routing = logic_response.json()
    except Exception as e:
        return {"error": "Logic agent failed", "details": str(e)}

    primary = routing.get("agent")
    next_agents = routing.get("next", [])

    results = {}

    try:
        primary_url = f"http://{primary}:{AGENT_PORTS[primary]}/run"
        primary_result = requests.post(primary_url, json={"prompt": prompt})
        primary_result.raise_for_status()
        results[primary] = primary_result.json()
    except Exception as e:
        results[primary] = f"Error: {str(e)}"

    for agent in next_agents:
        try:
            agent_url = f"http://{agent}:{AGENT_PORTS[agent]}/run"
            follow_up = requests.post(agent_url, json={"prompt": prompt})
            follow_up.raise_for_status()
            results[agent] = follow_up.json()
        except Exception as e:
            results[agent] = f"Error: {str(e)}"

    summary_prompt = f"""
Pilot,
The following task was delegated: \"{prompt}\"
The results from the subsystems are as follows:
{results}

Summarize the mission outcome and report back with clarity.
"""
    summary = query_bt(summary_prompt)

    return {
        "routing": routing,
        "results": results,
        "summary": summary
    }
#DO MEMORY NEXT