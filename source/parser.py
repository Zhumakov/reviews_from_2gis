"""Модуль для парсинга html страниц 2GIS на отзывы."""

from bs4 import BeautifulSoup, Tag


USERNAME_CSS_SELECTOR = "div._1pi8bc0 > div._o7qbud > div._j1kt73 > div._m80g57y > span._14quei > \
span._wrdavn > span._16s5yj36"
DATE_CSS_SELECTOR = "div._1pi8bc0 > div._o7qbud > div._j1kt73 > div._m80g57y > div._a5f6uz"

# Варианты контейнера для отзыва и рейтинга
REVIEW_CONTAINER_CSS_SELECTORS = ("div._1i94jn5", "div._1pi8bc0")
REVIEW_CSS_SELECTOR = "div._49x36f > a"
RATING_CSS_SELECTOR = "div._92aljh > div._1m0m6z5 > div._1fkin5c"


class ParserError(Exception):
    """Представляет собой ошибки парсинга страницы."""


class ReviewesParser:
    """Парсер для html страницы 2GIS."""

    def __init__(self, html_content: str) -> None:
        """
        Создаёт объект парсера с html кодом страницы.

        Args:
            html_content: html код страницы

        """
        self.html_content = html_content

    def get_rewiews(self) -> list[dict[str, str]]:
        """
        Парсит html страницу и вытаскивает из неё все отзывы в виде словаря.

        Returns:
            Поля:
                username: имя пользователя
                review: текст отзыва
                rating: рейтинг, поставленный пользователем

        Raises:
            ParserError:
                Ошибки при парсинге, связанные с неожиданной структурой

        """
        soup = BeautifulSoup(self.html_content, "lxml")
        tab_navigator = soup.select_one("div._qvsf7z")

        if tab_navigator is None:
            err_msg = "На странице не найдена вкладка с отзывами"
            raise ParserError(err_msg)

        rewiews_tab = tab_navigator.find_parents("div")
        if len(rewiews_tab) < 2:
            err_msg = "Вкладка с отзывами изменила структуру"
            raise ParserError(err_msg)

        rewiews_container = rewiews_tab[1]
        rewiews = rewiews_container.select("div._1k5soqfl")

        list_rewiews: list[dict[str, str]] = []
        for rewiew in rewiews:
            rewiew_field = self.__parse_review_fields(rewiew)
            list_rewiews.append(rewiew_field)

        return list_rewiews

    def __parse_review_fields(self, review_block: Tag) -> dict[str, str]:
        """
        Парсит блок отзыва, вытаскивая из него имя пользователя, текст отзыва и рейтинг.

        Args:
            review_block: блок отзыва

        Returns:
            Словарь с полями отзыва

        Raises:
            ParserError:
                Ошибки при парсинге, связанные с неожиданной структурой

        """
        username = review_block.select_one(USERNAME_CSS_SELECTOR)
        if username is None:
            msg_error = "Не удалось найти имя пользователя"
            raise ParserError(msg_error)

        date = review_block.select_one(DATE_CSS_SELECTOR)
        if date is None:
            msg_error = "Не удалось найти дату отзыва"
            raise ParserError(msg_error)

        for review_container in REVIEW_CONTAINER_CSS_SELECTORS:
            review = review_block.select_one(f"{review_container} > {REVIEW_CSS_SELECTOR}")
            if review is not None:
                break
        else:
            msg_error = "Не удалось найти текст отзыва"
            raise ParserError(msg_error)

        for review_container in REVIEW_CONTAINER_CSS_SELECTORS:
            rating = review_block.select_one(f"{review_container} > {RATING_CSS_SELECTOR}")
            if rating is not None:
                rating = str(len(rating.select("span")))
                break
        else:
            msg_error = "Не удалось найти оценку"
            raise ParserError(msg_error)

        return {
            "username": username.text,
            # Убрать метку если отзыв был отредактирован
            "date": date.text.rstrip(", отредактирован"),
            "review": review.text,
            "rating": rating,
        }
