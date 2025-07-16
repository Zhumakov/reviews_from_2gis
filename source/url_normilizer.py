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

    def normilize(self, url: str) -> str:
        """
        Нормализует url, чтобы он указывал на вкладку с отзывами.

        Args:
            url: исходный адрес

        Returns:
            Измененный адрес, или исходный если он является верным

        Raises:
            ValueError: Неправильная ссылка

        """
        # Проверяет, является ли исходный url правильным эндпоинтом
        # он должен оканчиваться например на /tab/reviews
        endpoint_pattern = re.compile(f"https://.*{self.review_endpoint}[^/]*")
        if endpoint_pattern.fullmatch(url):
            return url

        firm_id_pattern = re.compile(r"(https://.*/firm/\d+).*")
        firm_page = firm_id_pattern.fullmatch(url)
        if not firm_page:
            err_msg = f"Неправильная ссылка! URL: {url}"
            raise ValueError(err_msg)

        firm_page = firm_page.group(1)
        return firm_page + self.review_endpoint
