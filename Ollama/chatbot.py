import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2:3b"


def generate_reply(messages: list[dict[str, str]]) -> str:
    payload = {"model": MODEL, "messages": messages, "stream": False}
    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        reply = json.load(response)["message"]["content"]
    if not isinstance(reply, str) or not reply.strip():
        raise ValueError("Ollama повернула порожню або некоректну відповідь.")
    return reply


def main():
    history: list[dict[str, str]] = []
    print(f"Локальний чат з {MODEL}. Введіть Bye, щоб вийти.")

    while True:
        try:
            prompt = input("Ви: ").strip()
            if prompt.casefold() == "bye":
                break
            if not prompt:
                continue

            user_message = {"role": "user", "content": prompt}
            reply = generate_reply([*history, user_message])
        except (EOFError, KeyboardInterrupt):
            print("Вихід з чату. KeyboardInterrupt або EOFError.")
            break
        except Exception as error:
            print(f"Помилка: {error}")
            continue

        history.extend([user_message, {"role": "assistant", "content": reply}])
        print(f"Бот: {reply}")

    print("До побачення!")


if __name__ == "__main__":
    main()
