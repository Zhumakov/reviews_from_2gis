"""Модуль с тестами для парсеров."""

import pytest

from source.parser import ReviewesParser


@pytest.mark.parametrize(
    ("plained_comment"),
    [
        "очень грязно, не убирают особо, картошка сухая и мелкая, бургер норм был, "
        "ну как то вообще не очень, обходите стороной",
        # -------SECOND-------
        "Чисто и вкусно",
    ],
)
async def test_review_parser(plained_comment: str, html_content: str) -> None:
    """
    Тестирует парсер для отзывов.

    Args:
        plained_comment: существующий на странице комментарий
        html_content: html код страницы

    Raises:
        AssertionError: Ошибка парсера

    """
    assert plained_comment in html_content, "Планируемого отзыва не найдено"
    parser = ReviewesParser(html_content)
    comments: list[dict[str, str]] = parser.get_comments()

    assert comments, "Отзывы не были найдены"

    for comment in comments:
        if plained_comment in comment.get("review", ""):
            assert True
            break
    else:
        raise AssertionError("Ожидаемого отзыва не найдено")
