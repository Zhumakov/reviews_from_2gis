import re


class UrlNormilizer:
    """Исправляет ссылки, если они не указывают на вкладку с отзывами."""

    def __init__(self, review_endpoint: str) -> None:
        """
        Создаёт Normilizer с заданными эндпоинтом для отзывов.

        Args:
            review_endpoint: эндпоинт для отзывов

        """
        self.review_endpoint = review_endpoint

    def normilize(self, url: str) -> tuple[str, str]:
        """
        Нормализует url, чтобы он указывал на вкладку с отзывами.

        Args:
            url: исходный адрес

        Returns:
            Tuple:
                1 - url адрес на вкладку с отзывами,
                2 - id организации

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
        return firm_url + self.review_endpoint, firm_id
