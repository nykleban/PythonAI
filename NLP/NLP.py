import json
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Завантаження ресурсів
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Вхідні відгуки (можна замінити на ваші дані з Browse AI)
reviews = [
    "Dogs were running outside!",
    "Too small, would prefer a mat for a work surface that was anti static.",
    "Excellent quality, absolutely love it! Fast delivery.",
    "Very bad experience, broken on arrival and terrible support.",
    "It works fine, nothing special.",
]

results = []
sentiments = []

# Обробка відгуків (NLP + TextBlob)
for text in reviews:
    # Токенізація та очищення
    words = word_tokenize(text)
    clean_words = [ w for w in words if w.isalpha() and w.lower() not in stop_words]

    # Стеммінг та лематизація
    stemmed = [stemmer.stem(w) for w in clean_words]
    lemmatized = [lemmatizer.lemmatize(w.lower()) for w in clean_words]

    # Визначення тональності за допомогою TextBlob
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    sentiments.append(sentiment)
    results.append(
        {
            "text": text,
            "tokens": words,
            "stemmed": stemmed,
            "lemmatized": lemmatized,
            "sentiment": sentiment,
        }
    )

# Збереження результатів у JSON
with open("reviews_processed.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Підрахунок та побудова діаграми
counts = {
    "Positive": sentiments.count("Positive"),
    "Neutral": sentiments.count("Neutral"),
    "Negative": sentiments.count("Negative"),
}

colors = ["#2ecc71", "#95a5a6", "#e74c3c"]
plt.figure(figsize=(7, 4))
plt.bar(counts.keys(), counts.values(), color=colors)
plt.title("Кількість позитивних, нейтральних та негативних відгуків")
plt.xlabel("Тональність")
plt.ylabel("Кількість")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()