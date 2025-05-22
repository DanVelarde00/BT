#!/usr/bin/env python3
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI(title="BT", description="BT is a construct that builds things based on user requests, integrating local LLMs.")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head><title>BT - Build Things</title></head>
        <body>
            <h1>BT</h1>
            <p>Hello, Commander. I'm BT, your dedicated assistant for building things.</p>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(content)
    return {"message": f"File '{file.filename}' received and saved.", "path": file_path}

@app.post("/execute")
async def execute_command(command: str = Form(...)):
    # This endpoint is a placeholder for processing user commands.
    # Integration with local LLMs and repository operations will be added.
    response_message = f"Processing command: {command}"
    return {"response": response_message}

def speak(text: str):
    # Stub for text-to-speech. In the future, integrate with a TTS engine.
    print(f"BT says: {text}")

if __name__ == '__main__':
    speak("Booting up! Ready to build things, Commander.")
    uvicorn.run(app, host="0.0.0.0", port=8080)
