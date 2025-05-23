# BT: Modular AI System

BT is a modular multi-agent AI system designed to delegate and coordinate tasks across specialized subsystems. It provides a flexible architecture for building, planning, coding, and evaluating solutions using large language models (LLMs).

## Architecture

The repository is organized into the following components:

- **orchestrator**: FastAPI service that receives user prompts and delegates tasks according to the Decision Protocol.
- **logic**: FastAPI service that determines routing (which agent should handle the instruction first and any follow-ups).
- **planner**: FastAPI service for generating high-level plans.
- **coder**: FastAPI service for writing and generating code.
- **critic**: FastAPI service for reviewing and critiquing outputs.
- **bt-ui**: React + Vite frontend for interacting with the system.
- **frontend**: Tailwind CSS and PostCSS configuration for styling.
- **docker-compose.yml**: Defines multi-container setup for local development.

## Prerequisites

- Docker & Docker Compose
- Node.js & npm (for \`bt-ui\`)
- Python 3.8+ & pip (optional, if running services locally)

## Setup

1. Copy env file:

   ```bash
   cp .env.example .env
   ```

2. (Optional) Configure environment variables in \`.env\` and in each service’s \`.env\` file.

## Running with Docker Compose

Build and start all services:

```bash
# From the project root
docker-compose up --build
```

Services will be available at:

- Orchestrator:  \`http://localhost:8000/orchestrate\`
- Planner:       \`http://localhost:8001/run\`
- Coder:         \`http://localhost:8002/run\`
- Critic:        \`http://localhost:8003/run\`
- Logic:         \`http://localhost:8005/route\`

## Running Locally

### Backend Services

```bash
# Example: Orchestrator
cd orchestrator
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Repeat for other services, adjusting ports and directories.

### Frontend UI

```bash
cd bt-ui
npm install
npm run dev -- --host 0.0.0.0
```

Access the UI at \`http://localhost:5173\`.

## Usage

Send a prompt to the orchestrator endpoint:

```bash
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your question or task"}'
```

## Contributing

Pull requests are welcome. Please ensure code quality and tests where applicable.

## License

Specify license here.
