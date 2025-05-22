#!/usr/bin/env python3
import argparse
import requests
import sys


def run_locallai(command: str):
    """Placeholder for localAi integration. Assumes localAi API is running at http://localhost:5001/api."""
    url = "http://localhost:5001/api"
    data = {"prompt": command}
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def run_ollama(command: str):
    """Placeholder for Ollama integration. Assumes Ollama API is running at http://localhost:5002/api."""
    url = "http://localhost:5002/api"
    data = {"prompt": command}
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Execute commands using local LLMs")
    parser.add_argument("--backend", choices=["locallai", "ollama"], required=True, help="Which LLM backend to use")
    parser.add_argument("--command", required=True, help="The command to send to the LLM")
    args = parser.parse_args()

    if args.backend == "locallai":
        result = run_locallai(args.command)
    elif args.backend == "ollama":
        result = run_ollama(args.command)
    else:
        print("Invalid backend provided")
        sys.exit(1)
    
    print("LLM Response:")
    print(result)


if __name__ == "__main__":
    main()
