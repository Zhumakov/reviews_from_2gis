"""Модуль для парсинга html страниц 2GIS на отзывы."""

from bs4 import BeautifulSoup, Tag


USERNAME_CSS_SELECTOR = "span._16s5yj36"
DATE_CSS_SELECTOR = "div._a5f6uz"

NUMBER_OF_REVIEWS_CSS_SELECTOR = "span._1xhlznaa"
TAB_NAVIGATOR_CSS_SELECTOR = "div._qvsf7z"
REVIEW_CSS_SELECTOR = "div._49x36f > a"
RATING_CSS_SELECTOR = "div._1fkin5c"


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

    def get_rewiews(self, last_saved_review: int = 0) -> list[dict[str, str]]:
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
        tab_navigator = soup.select_one(TAB_NAVIGATOR_CSS_SELECTOR)
        if tab_navigator is None:
            err_msg = "На странице не найдена вкладка с отзывами"
            raise ParserError(err_msg)

        number_of_reviews = tab_navigator.select_one(NUMBER_OF_REVIEWS_CSS_SELECTOR)
        if number_of_reviews is None:
            err_msg = "Не найдена информация о количестве отзывов"
            raise ParserError

        number_of_reviews = int(number_of_reviews.text)
        number_of_new_reviews = number_of_reviews - last_saved_review

        reviews_tab = tab_navigator.find_parents("div")
        if len(reviews_tab) < 2:
            err_msg = "Вкладка с отзывами изменила структуру"
            raise ParserError(err_msg)

        reviews_container = reviews_tab[1]
        reviews = reviews_container.select("div._1k5soqfl")
        if len(reviews) < number_of_new_reviews:
            err_msg = "Количество отзывов на странице, меньше чем новых отзывов"
            raise ParserError(err_msg)

        list_reviews: list[dict[str, str]] = []
        for rewiew in reviews[:number_of_new_reviews]:
            rewiew_field = self.__parse_review_fields(rewiew)
            list_reviews.append(rewiew_field)

        return list_reviews

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

        review = review_block.select_one(REVIEW_CSS_SELECTOR)
        if review is None:
            msg_error = "Не удалось найти текст отзыва"
            raise ParserError(msg_error)

        rating = review_block.select_one(RATING_CSS_SELECTOR)
        if rating is None:
            msg_error = "Не удалось найти оценку"
            raise ParserError(msg_error)
        rating = str(len(rating.select("span")))

        return {
            "username": username.text,
            # Убрать метку если отзыв был отредактирован
            "date": date.text.rstrip(", отредактирован"),
            "review": review.text,
            "rating": rating,
        }
