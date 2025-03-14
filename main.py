import requests
import os
from urllib.parse import urlparse


def shorten_link(token, url):
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "url": url,
        "access_token": token,
        "v": "5.131",
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["response"]["short_url"]


def count_clicks(short_url, token):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    parsed_url = urlparse(short_url)
    path = parsed_url.path
    key = path[1:]
    params = {"key": key, "access_token": token, "v": "5.131", "extended": 1}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    stats = data["response"]["stats"]
    clicks = sum(day["views"] for day in stats)
    return clicks


def is_shorten_link(url):
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
