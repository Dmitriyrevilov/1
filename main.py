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
    response_dict = response.json()
    if "error" in response_dict:
        raise requests.exceptions.RequestException(response_dict["error"]["error_msg"])
    return response_dict["response"]["short_url"]


def count_clicks(token, short_url):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip("/")
    params = {"key": key, "access_token": token, "v": "5.131", "extended": 1}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_dict = response.json()
    if "error" in response_dict:
        raise requests.exceptions.RequestException(response_dict["error"]["error_msg"])
    stats = response_dict["response"]["stats"]
    clicks = sum(day["views"] for day in stats)
    return clicks


def is_shorten_link(token, url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc != "vk.cc":
            return False
        key = parsed_url.path.lstrip("/")
        api_url = "https://api.vk.com/method/utils.getLinkStats"
        params = {"key": key, "access_token": token, "v": "5.131"}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_dict = response.json()
        if "error" in response_dict:
            return False
        return True
    except requests.exceptions.RequestException:
        return False


if __name__ == "__main__":
    url = input("Введите ссылку: ")
    try:
        token = os.environ["VK_TOKEN"]
    except KeyError:
        print("Ошибка: Не указана переменная окружения VK_TOKEN.")
    try:
        if is_shorten_link(token, url):
            clicks = count_clicks(token, url)
            print("Переходы:", clicks)
        else:
            short_url = shorten_link(token, url)
            print("Сокращенная ссылка:", short_url)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
