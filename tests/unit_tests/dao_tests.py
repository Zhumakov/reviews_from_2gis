from aiosqlite import IntegrityError
import pytest

from source.dao import ReviewsDAO
from tests.conftest import TEST_URL, TEST_FIRM_ID


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
            TEST_FIRM_ID,
        )
        assert not fail
    except IntegrityError:
        assert fail


@pytest.mark.parametrize(
    ("firm_id_to_insert", "firm_id_to_get", "plained_ordinal_number"),
    [("1", "1", 1), ("2", "99999999", 0)],
)
async def test_get_last_review(
    firm_id_to_insert: str,
    firm_id_to_get: str,
    plained_ordinal_number: str,
    reviews_dao: ReviewsDAO,
) -> None:
    await reviews_dao.insert_review(
        {"username": "Некто", "date": "1 октября 295", "review": "Ещё не открылся", "rating": 1},
        1,
        firm_id_to_insert,
    )

    last_ordinal_number = await reviews_dao.get_last_insert_review(firm_id_to_get)
    assert last_ordinal_number == plained_ordinal_number
