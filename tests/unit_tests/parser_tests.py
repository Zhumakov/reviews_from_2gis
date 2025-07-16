"""Модуль с тестами для парсеров."""

import sys

import pytest

from source.parser import ReviewesParser


@pytest.mark.parametrize(
    ("plained_username", "plained_date", "plained_comment", "plained_rating"),
    [
        (
            "кира ракова",
            "17 июня 2025",
            # -----REVIEW------
            "очень грязно, не убирают особо, картошка сухая и мелкая, бургер норм был, "
            "ну как то вообще не очень, обходите стороной",
            # -----REVIEW------
            "2",
        ),
        ("Емеля Емеля", "23 июня 2025", "Чисто и вкусно", "5"),
    ],
)
async def test_review_parser(
    plained_username: str,
    plained_date: str,
    plained_comment: str,
    plained_rating: str,
    html_content: str,
) -> None:
    """
    Тестирует парсер для отзывов.

    Args:
        plained_username: планируемое имя пользователя
        plained_date: планируемая дата отзыва
        plained_comment: планируемый текст отзыва
        plained_rating: планируемый рейтинг
        html_content: html код страницы

    """
    parser = ReviewesParser(html_content)
    comments: list[dict[str, str]] = parser.get_rewiews()

    assert comments, "Отзывы не были найдены"

    for comment in comments:
        if plained_comment in comment.get("review", ""):
            assert plained_date in comment.get("date", "")
            assert plained_username in comment.get("username", "")
            assert plained_rating in comment.get("rating", "")
            break
    else:
        pytest.fail("Ожидаемого отзыва не найдено")
