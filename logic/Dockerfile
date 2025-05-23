# logic/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "logic_main:app", "--host", "0.0.0.0", "--port", "8005"]
COPY .env /app/.env
ENV LLM_API_URL = os.getenv("LM_API_URL", "http://host.docker.internal:11434")

