import requests
import os
from urllib.parse import urlparse


def shorten_link(token, url):  # Название функции с параметрами token,url
    api_url = "https://api.vk.com/method/utils.getShortLink"  # Формируем URL для запроса к VK API (utils.getShortLink)
    params = {
        "url": url,
        "access_token": token,
        "v": "5.131",
    }  # параметры c url- это ссылка, которую мы будем вводить в input
    response = requests.get(
        api_url, params=params
    )  # Отправляем GET заппрос к VK API с помощью requests.get
    response.raise_for_status()  # Проверка на ошибки
    data = response.json()  # Перевели JSON ответ сервера и записали в переменную data
    return data["response"]["short_url"]  # извлекли сокращенную ссылку из ответа JSON


def count_clicks(short_url, token):
    api_url = "https://api.vk.com/method/utils.getLinkStats"  # Формируем URL для запроса к VK API (utils.getLinkStats)
    parsed_url = urlparse(short_url)  # Парсим URL
    path = parsed_url.path  # Извлекаем key из короткой ссылки
    key = path[1:]  # убираем первый символ /
    params = {"key": key, "access_token": token, "v": "5.131", "extended": 1}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    stats = data["response"]["stats"]
    clicks = sum(
        day["views"] for day in stats
    )  # вычисления суммы просмотров (views) для каждого дня в списке stats
    return clicks


def is_shorten_link(url):
    """Проверяет, является ли URL сокращенной ссылкой vk.cc."""
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc"


if __name__ == "__main__":
    url = input("Введите ссылку: ")
    token = os.getenv("API_TOKEN")
    try:
        short_url = shorten_link(token, url)
        print("Сокращенная ссылка:", short_url)
        clicks = count_clicks(short_url, token)
        print("Переходы", clicks)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
