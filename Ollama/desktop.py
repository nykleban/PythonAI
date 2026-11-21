import tkinter as tk
from queue import SimpleQueue
from threading import Thread
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from chatbot import MODEL, generate_reply


def main() -> None:
    window = tk.Tk()
    window.title(f"Локальний чат --- {MODEL} ---")
    window.geometry("640x440")

    transcript = ScrolledText(window, wrap="word", state="disabled")
    transcript.pack(fill="both", expand=True, padx=12, pady=(12, 8))

    controls = ttk.Frame(window)
    controls.pack(fill="x", padx=12)
    entry = ttk.Entry(controls)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

    status = tk.StringVar(value="Введіть Bye, щоб закрити чат.")
    ttk.Label(window, textvariable=status).pack(anchor="w", padx=12, pady=(4, 12))

    history: list[dict[str, str]] = []
    results: SimpleQueue[str | Exception] = SimpleQueue()
    pending_message: dict[str, str] | None = None

    def append_message(author: str, message: str) -> None:
        transcript.configure(state="normal")
        transcript.insert("end", f"{author}: {message}\n\n")
        transcript.configure(state="disabled")
        transcript.see("end")

    def request_reply(messages: list[dict[str, str]]) -> None:
        try:
            results.put(generate_reply(messages))
        except Exception as error:
            results.put(error)

    def show_reply() -> None:
        nonlocal pending_message
        if results.empty():
            window.after(100, show_reply)
            return

        result = results.get_nowait()
        if isinstance(result, Exception):
            append_message("Помилка", str(result))
        elif pending_message is not None:
            history.extend([pending_message, {"role": "assistant", "content": result}])
            append_message("Бот", result)
        pending_message = None
        status.set("Введіть Bye, щоб закрити чат.")

    def send_message(event: tk.Event | None = None) -> None:
        nonlocal pending_message
        prompt = entry.get().strip()
        if prompt.casefold() == "bye":
            window.destroy()
            return
        if not prompt or pending_message is not None:
            return

        entry.delete(0, "end")
        entry.focus_set()
        append_message("Ви", prompt)
        status.set("Очікую відповідь від Ollama…")
        pending_message = {"role": "user", "content": prompt}
        messages = [*history, pending_message]
        Thread(target=request_reply, args=(messages,), daemon=True).start()
        window.after(100, show_reply)

    ttk.Button(controls, text="Надіслати", command=send_message).pack(side="right")
    entry.bind("<Return>", send_message)
    entry.focus_set()
    window.mainloop()


if __name__ == "__main__":
    main()
