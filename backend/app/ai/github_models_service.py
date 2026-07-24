import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_MODELS_URL = "https://models.inference.ai.azure.com/chat/completions"


def call_github_models(
    prompt: str,
    system_prompt: str = "You are Dr. Vaidya, an expert medical report interpreter.",
    model: str = "Meta-Llama-3.3-70B-Instruct"
) -> str:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not set")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": model,
        "temperature": 0.2
    }

    response = requests.post(GITHUB_MODELS_URL, headers=headers, json=payload, timeout=25)

    if response.status_code != 200:
        raise Exception(f"GitHub Models Error ({response.status_code}): {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
