import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import lxml
import aiohttp
import logging
import random
import time
from functools import lru_cache, wraps
from datetime import datetime, timedelta, timezone

logging.basicConfig(filename="logs.log", filemode='a', level=logging.ERROR,
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s")  # настройка логирования


# декоратор для кеширования lru_cache
def cache_decorator(seconds: int = 600, maxsize: int = 128):
    def wrapper_cache(func):
        # выбор даты истечения срока кеша(случайное время в секундах от 10 минут до 25 минут)
        seconds = random.randint(600, 1500)
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now(timezone.utc) + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now(timezone.utc) >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.now(timezone.utc) + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func
    return wrapper_cache


class WeatherDataFetcher:
    def __init__(self, url: str = 'https://sheremetyevo.aeroport.website/pogoda'):
        """
        Конструктор класса. Принимает URL веб-ресурса с информацией о погоде.

        Параметры:
        url (строка): URL-адрес веб-ресурса (по умолчанию используется сайт https://sheremetyevo.aeroport.website/pogoda).
        """
        self.url = url
        self.response = None
        self.bs = None

    @cache_decorator()
    async def fetch_data(self):
        mobile_viewports_width = [
            '320', '375', '390', '414', '360',
            '412', '393', '384', '480', '600', '768', '800', '962'
        ]

        mobile_viewports_height = [
            '568', '667', '844', '896', '640', '732', '851', '854', '960', '1024', '1180'
        ]

        accept_language = [
            'en-US,en;q=0.9', 'en-GB,en;q=0.9',
            'en-CA,en;q=0.9', 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        ]

        parsing_headers = {
            'User-Agent': UserAgent().random,
            'viewport-width': random.choice(mobile_viewports_width),
            'viewport-height': random.choice(mobile_viewports_height),
            'Connection': 'keep-alive',
            'Accept-Language': random.choice(accept_language),
            'Cache-Control': 'max-age=0',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=parsing_headers) as response:
                response.raise_for_status()
                self.response = await response.text()
        await session.close()

    def parse_data(self):
        """
        Метод для парсинга полученных данных о погоде.

        Парсит HTML-код страницы с данными и сохраняет их в формате BeautifulSoup.
        """
        try:
            self.bs = BeautifulSoup(self.response, "lxml")
        except (aiohttp.ClientError, AttributeError) as e:
            logging.error(f"Error parsing data: {e}")

    def get_temperature(self) -> str:
        """
        Метод для получения текущей температуры.

        Возвращает строковое значение текущей температуры.
        """
        return self.bs.find_all('div', 'weather-cont__info')[0].find('div').find_all('span')[0].text

    def get_temperature_status(self) -> str:
        """
        Метод для получения статуса температуры.

        Возвращает строковое значение статуса температуры (например, "ясно").
        """
        return (self.bs.find_all('div', 'weather-cont__info')[0].find('div').find_all('span')[1].text).replace(",", "")

    def get_wind(self) -> str:
        """
        Метод для получения информации о скорости ветра.

        Возвращает строковое значение скорости ветра.
        """
        return self.bs.find_all('span', 'wind__txt')[0].text

    def get_air_pressure(self) -> str:
        """
        Метод для получения значения атмосферного давления.

        Возвращает строковое значение атмосферного давления.
        """
        return (self.bs.find_all('div', 'weather-more')[0].find_all("span")[2].text).replace("давление: ", "")


if __name__ == "__main__":
    url = 'https://sheremetyevo.aeroport.website/pogoda'

    weather_fetcher = WeatherDataFetcher(url)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(weather_fetcher.fetch_data())
    weather_fetcher.parse_data()

    temperature = weather_fetcher.get_temperature()
    # print(temperature)
    temp_status = weather_fetcher.get_temperature_status()
    # print(temp_status)
    wind = weather_fetcher.get_wind()
    # air_pressure = weather_fetcher.get_air_pressure()

    print(f"'{temp_status}', '{temperature}', '{wind}'")
