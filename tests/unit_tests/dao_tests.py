from aiosqlite import IntegrityError
import pytest

from source.dao import ReviewsDAO
from tests.conftest import TEST_URL


@pytest.mark.parametrize(
    ("ordinal_numer", "review_data", "fail"),
    [
        (
            1,
            {
                "username": "Андрей",
                "date": "17 июля 2025",
                "review": "Сытно и вкусно",
                "rating": "5",
            },
            False,
        ),
        (
            2,
            {
                "username": "Максим",
                "date": "17 июля 2025",
                "review": "Невкусно",
                "rating": "1",
            },
            False,
        ),
        (
            1,
            {
                "username": "Роман",
                "date": "17 июля 2025",
                "review": "Какой-то другой отзыв",
                "rating": "5",
            },
            True,
        ),
        (
            3,
            {
                "username": None,
                "date": "17 июля 2025",
                "review": "Сытно и вкусно",
                "rating": "5",
            },
            True,
        ),
        (
            4,
            {
                "username": "Андрей",
                "date": None,
                "review": "Сытно и вкусно",
                "rating": "5",
            },
            True,
        ),
        (
            5,
            {
                "username": "Андрей",
                "date": "17 июля 2025",
                "review": None,
                "rating": "5",
            },
            True,
        ),
        (
            6,
            {
                "username": "Андрей",
                "date": "17 июля 2025",
                "review": "Сытно и вкусно",
                "rating": "0",
            },
            True,
        ),
    ],
)
async def test_review_insert(
    ordinal_numer: int,
    review_data: dict,
    fail: bool,
    reviews_dao: ReviewsDAO,
) -> None:
    """
    Проверяет ограничения таблицы и вставку значений в неё.

    Args:
        ordinal_numer: порядковый номер отзыва
        review_data: данные об отзыве
        fail: ожидается ли провал вставки отзыва в таблицу
        reviews_dao: объект для работы с бд

    """
    try:
        await reviews_dao.insert_review(
            review_data,
            ordinal_numer,
            TEST_URL,
        )
        assert not fail
    except IntegrityError:
        assert fail
