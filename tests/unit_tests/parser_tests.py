"""Модуль с тестами для парсеров."""

import pytest

from source.parser import ReviewesParser


@pytest.mark.parametrize(
    ("plained_username", "plained_comment", "plained_rating"),
    [
        (
            "кира ракова",
            # -----REVIEW------
            "очень грязно, не убирают особо, картошка сухая и мелкая, бургер норм был, "
            "ну как то вообще не очень, обходите стороной",
            # -----REVIEW------
            "2",
        ),
        ("Емеля Емеля", "Чисто и вкусно", "5"),
    ],
)
async def test_review_parser(
    plained_username: str, plained_comment: str, plained_rating: str, html_content: str
) -> None:
    """
    Тестирует парсер для отзывов.

    Args:
        plained_username: планируемое имя пользователя
        plained_comment: планируемый текст отзыва
        plained_rating: планируемый рейтинг
        html_content: html код страницы

    Raises:
        AssertionError: Ошибка парсера

    """
    assert plained_username in html_content
    assert plained_rating in html_content
    parser = ReviewesParser(html_content)
    comments: list[dict[str, str]] = parser.get_rewiews()

    assert comments, "Отзывы не были найдены"

    for comment in comments:
        if plained_comment in comment.get("review", ""):
            assert plained_username in comment.get("username", "")
            assert plained_rating in comment.get("rating", "")
            break
    else:
        raise AssertionError("Ожидаемого отзыва не найдено")
