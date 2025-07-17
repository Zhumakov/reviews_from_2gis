"""Модуль для начальной конфигурации тестов."""

from typing import AsyncGenerator

import pytest

from source.dao import ReviewsDAO


TEST_PAGE = "tests/first_page.html"
TEST_URL = "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/tab/reviews"
TEST_FIRM_ID = "70000001057550594"
TEST_DB_NAME = "test.db"


@pytest.fixture(scope="session")
def html_content() -> str:
    """
    Возвращает html страницу тестового url страницы.

    Returns:
        html код страница

    """
    with open(TEST_PAGE, "r", encoding="utf8") as file:
        return file.read()


@pytest.fixture(scope="session")
async def reviews_dao() -> AsyncGenerator[ReviewsDAO]:
    """
    Создаёт базу данных и таблицу перед тестами, затем удаляет их.

    Yields:
        объект класса ReviewsDAO

    """
    dao = ReviewsDAO(TEST_DB_NAME)
    await dao.setup_db()
    yield dao
    await dao.delete_db()
