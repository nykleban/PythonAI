# /// script
# dependencies = ["python-dotenv", "requests"]
# ///

import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def get_ai_response(user_text):
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Відповідай коротко й українською."},
                {"role": "user", "content": user_text},
            ],
            "temperature": 0.7,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def main():
    if not API_KEY:
        raise SystemExit("Додай ключ Groq у API_KEY або GROQ_API_KEY у файлі Ollama/.env.")

    print("Чат Groq. Введи exit, щоб вийти.")
    while True:
        user_text = input("Ти: ").strip()
        if user_text.lower() == "exit":
            break
        if not user_text:
            continue

        try:
            print(f"Бот: {get_ai_response(user_text)}")
        except requests.RequestException as error:
            print(f"Помилка Groq: {error}")

    print("До побачення!")


if __name__ == "__main__":
    main()
