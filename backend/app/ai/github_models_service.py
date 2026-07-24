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

    models_to_try = [model, "Meta-Llama-3.3-70B-Instruct", "gpt-4o-mini", "Phi-3.5-mini-instruct"]

    last_error = None
    for m in models_to_try:
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
            "model": m,
            "temperature": 0.2
        }

        try:
            response = requests.post(GITHUB_MODELS_URL, headers=headers, json=payload, timeout=25)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                last_error = f"GitHub Models Error ({response.status_code}): {response.text}"
        except Exception as e:
            last_error = str(e)

    raise Exception(last_error or "GitHub Models call failed")
