import glob
import json
import os
import re
import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob

# Визначаємо поточну папку, де лежить цей скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))

# Автоматичний пошук завантаженого CSV-файлу від Rozetka
csv_files = glob.glob(os.path.join(current_dir, "*rozetka*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "Файл із відгуками Rozetka не знайдено у папці зі скриптом!"
    )

input_csv = csv_files[0]
print(f"Зчитуємо файл: {os.path.basename(input_csv)}")

df = pd.read_csv(input_csv)

# Стоп-слова для української мови
ukr_stopwords = {
    "і",
    "й",
    "та",
    "що",
    "це",
    "з",
    "із",
    "зі",
    "до",
    "у",
    "в",
    "на",
    "за",
    "про",
    "як",
    "так",
    "його",
    "її",
    "їх",
    "ми",
    "ви",
    "він",
    "вона",
    "вони",
    "але",
    "тому",
    "ніби",
    "був",
    "була",
    "було",
    "були",
    "не",
    "для",
    "по",
}


def ukr_stem(word):
    """Стеммінг: відсікання типових закінчень"""
    word = word.lower()
    for suffix in [
        "ого",
        "ому",
        "ими",
        "ий",
        "им",
        "ім",
        "их",
        "ів",
        "ами",
        "ах",
        "ою",
        "ею",
        "ам",
        "і",
        "а",
        "я",
        "у",
        "ю",
        "е",
        "є",
        "о",
    ]:
        if len(word) > 4 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


# Маркери для аналізу тональності відгуків
positive_markers = [
    "смачн",
    "топ",
    "чудов",
    "рекоменд",
    "радж",
    "непоган",
    "оригінальн",
    "цікав",
]
negative_markers = ["жахлив", "поган", "не рекомендую", "розбит", "підробк"]

processed_records = []
sentiments = []

for idx, row in df.iterrows():
    text = str(row["Comment Text"]).strip()
    author = row.get("Author", f"User_{idx+1}")

    # 1. Токенізація
    tokens = re.findall(r"\b\w+\b", text)

    # 2. Видалення стоп-слів
    filtered_tokens = [
        w for w in tokens if w.lower() not in ukr_stopwords and len(w) > 1
    ]

    # 3. Стеммінг
    stemmed = [ukr_stem(w) for w in filtered_tokens]

    # 4. Лематизація (нижній регістр / базова форма)
    lemmatized = [w.lower() for w in filtered_tokens]

    # Визначення тональності
    lower_text = text.lower()
    pos_score = sum(1 for m in positive_markers if m in lower_text)
    neg_score = sum(1 for m in negative_markers if m in lower_text)

    if pos_score > neg_score:
        polarity = 0.8
        sentiment = "Позитивний"
    elif neg_score > pos_score:
        polarity = -0.8
        sentiment = "Негативний"
    else:
        polarity = 0.0
        sentiment = "Нейтральний"

    sentiments.append(sentiment)
    processed_records.append(
        {
            "Position": row.get("Position", idx + 1),
            "Author": author,
            "Comment Text": text,
            "Tokens": tokens,
            "Filtered Tokens": filtered_tokens,
            "Stemmed": stemmed,
            "Lemmatized": lemmatized,
            "Polarity": polarity,
            "Sentiment": sentiment,
        }
    )

# 5. Збереження результатів у JSON та CSV
out_json = os.path.join(current_dir, "processed_rozetka_reviews.json")
out_csv = os.path.join(current_dir, "processed_rozetka_reviews.csv")

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(processed_records, f, ensure_ascii=False, indent=2)

pd.DataFrame(
    [
        {
            "Position": r["Position"],
            "Author": r["Author"],
            "Comment Text": r["Comment Text"],
            "Clean Words": " ".join(r["Filtered Tokens"]),
            "Stemmed": " ".join(r["Stemmed"]),
            "Polarity": r["Polarity"],
            "Sentiment": r["Sentiment"],
        }
        for r in processed_records
    ]
).to_csv(out_csv, index=False, encoding="utf-8")

print(f"Збережено JSON: {out_json}")
print(f"Збережено CSV: {out_csv}")

# 6. Побудова діаграми
counts = {
    "Позитивні": sentiments.count("Позитивний"),
    "Нейтральні": sentiments.count("Нейтральний"),
    "Негативні": sentiments.count("Негативний"),
}

plt.figure(figsize=(7, 4.5))
bars = plt.bar(
    counts.keys(), counts.values(), color=["#27ae60", "#95a5a6", "#e74c3c"]
)
plt.title("Розподіл відгуків з Rozetka за тональністю", fontsize=13)
plt.ylabel("Кількість відгуків", fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.1,
        str(int(h)),
        ha="center",
        va="bottom",
        fontweight="bold",
    )

plt.ylim(0, max(counts.values()) + 1.5)
plt.tight_layout()
plt.show()