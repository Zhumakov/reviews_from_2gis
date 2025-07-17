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
    reviews: list[dict[str, str]] = parser.get_rewiews()

    assert reviews, "Отзывы не были найдены"

    for review in reviews:
        if plained_comment in review.get("review", ""):
            assert plained_date in review.get("date", "")
            assert plained_username in review.get("username", "")
            assert plained_rating in review.get("rating", "")
            break
    else:
        pytest.fail("Ожидаемого отзыва не найдено")


@pytest.mark.parametrize(
    ("plained_username", "last_saved_review", "find"),
    [
        ("кира ракова", 88, False),
        ("Емеля Емеля", 88, True),
    ],
)
async def test_chunk_review_parser(
    plained_username: str,
    last_saved_review: int,
    find: bool,
    html_content: str,
) -> None:
    """
    Тестирует частичный парсинг отзывов со страницы.

    Args:
        plained_username: имя пользователя искомого отзыва
        find: должен ли быть найден отзыв
        html_content: html сраница с отзывами

    """
    parser = ReviewesParser(html_content)
    reviews: list[dict[str, str]] = parser.get_rewiews(last_saved_review)

    for review in reviews:
        if plained_username in review.get("username", ""):
            assert find
            break
    else:
        assert not find
