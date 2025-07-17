import re
from typing import NamedTuple


class UrlData(NamedTuple):
    """
    Представляет url данные.

    Attributes:
        reviews_url: url страницы с отзывами
        firm_id: id организации
    """

    reviews_url: str
    firm_id: str


class UrlNormilizer:
    """Исправляет ссылки, если они не указывают на вкладку с отзывами."""

    def __init__(self, review_endpoint: str) -> None:
        """
        Создаёт Normilizer с заданными эндпоинтом для отзывов.

        Args:
            review_endpoint: эндпоинт для отзывов

        """
        self.review_endpoint = review_endpoint

    def normilize(self, url: str) -> UrlData:
        """
        Нормализует url, чтобы он указывал на вкладку с отзывами.

        Args:
            url: исходный адрес

        Returns:
            UrlData

        Raises:
            ValueError: Неправильная ссылка

        """
        firm_id_pattern = re.compile(r"(https://.*/firm/(\d+)).*")
        firm_page = firm_id_pattern.fullmatch(url)
        if not firm_page:
            err_msg = f"Неправильная ссылка! URL: {url}"
            raise ValueError(err_msg)

        firm_url = firm_page.group(1)
        firm_id = firm_page.group(2)
        return UrlData(reviews_url=(firm_url + self.review_endpoint), firm_id=firm_id)
