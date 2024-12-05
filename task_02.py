import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

def fetch_text(url):
    """Завантажує текст із вказаної URL-адреси."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def map_words(text):
    """Функція Map: розбиває текст на слова та підраховує їх частоту."""
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def shuffle(counters):
    """Функція Shuffle: об'єднує результати від Map-функцій."""
    shuffled = Counter()
    for counter in counters:
        for word, count in counter.items():
            shuffled[word] += count
    return shuffled

def analyze_word_frequencies_with_shuffle(text, chunk_size=10000):
    """Аналіз частоти слів із фазами Map, Shuffle та Reduce."""
    # Розбиваємо текст на частини для паралельної обробки
    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    with ThreadPoolExecutor() as executor:
        # Фаза Map
        counters = list(executor.map(map_words, text_chunks))

    # Фаза Shuffle
    shuffled = shuffle(counters)

    # Результат після Reduce
    return shuffled

def visualize_top_words(word_freq, top_n=10):
    """Візуалізує топ-слова за частотою використання."""
    top_words = word_freq.most_common(top_n)
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()

def main():
    """Основна функція для виконання скрипта."""
    url = input("Введіть URL для завантаження тексту: ")

    print("Завантаження тексту...")
    try:
        text = fetch_text(url)
        print("Текст успішно завантажено.")

        print("Аналіз частоти слів...")
        word_frequencies = analyze_word_frequencies_with_shuffle(text)
        print("Аналіз завершено.")

        print("Візуалізація топ-10 найчастіших слів...")
        visualize_top_words(word_frequencies, top_n=10)
        print("Готово!")
    except Exception as e:
        print(f"Сталася помилка: {e}")

if __name__ == "__main__":
    main()
