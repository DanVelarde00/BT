#!/usr/bin/env python3
import argparse
import re
import sys
import requests


def extract_code_blocks(text: str) -> str:
    """Extracts code blocks enclosed in triple backticks from the user input.
    If no code blocks are found, returns the entire input trimmed."""
    matches = re.findall(r"```(.+?)```", text, re.DOTALL)
    if matches:
        return "\n\n".join(match.strip() for match in matches)
    return text.strip()


def send_to_openhands(repo: str, branch: str, new_repo: bool, code: str) -> dict:
    """Sends the extracted code along with repository info to the OpenHands API."""
    # Assuming OpenHands API endpoint is available at the following URL
    url = "http://localhost:8080/execute"
    payload = {
        "repo": repo,
        "branch": branch,
        "new_repo": new_repo,
        "code": code
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def read_user_input() -> str:
    """Reads multi-line user input until an empty line is encountered."""
    print("Enter your instruction (press Enter twice when done):")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Agent: Process user input and send coding instructions to OpenHands API."
    )
    parser.add_argument("--repo", required=True, help="Repository name (e.g., 'username/repo') or identifier for a new repository.")
    parser.add_argument("--branch", required=True, help="Branch where the output should be saved.")
    parser.add_argument("--new-repo", action="store_true", help="Flag indicating that a new repository should be created.")
    args = parser.parse_args()

    user_text = read_user_input()
    code_content = extract_code_blocks(user_text)
    print("\nExtracted code relevant to coding:")
    print(code_content)

    print("\nSending to OpenHands API...")
    result = send_to_openhands(args.repo, args.branch, args.new_repo, code_content)
    print("\nResponse from OpenHands API:")
    print(result)


if __name__ == "__main__":
    main()
