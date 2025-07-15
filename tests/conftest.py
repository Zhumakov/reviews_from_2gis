"""Модуль для начальной конфигурации тестов."""

import pytest


TEST_PAGE = "tests/test_page.html"


@pytest.fixture(scope="session")
def html_content() -> str:
    """
    Возвращает html страницу тестового url страницы.

    Returns:
        html код страница

    """
    with open(TEST_PAGE, "r", encoding="utf8") as file:
        return file.read()
