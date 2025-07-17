"""Модуль для тестирования html_fetcher."""

import pytest

from source.html_fetcher import HtmlFetcher
from tests.conftest import TEST_URL


@pytest.mark.parametrize(
    ("url", "plained_review", "last_plained_review", "fail"),
    [
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/tab/reviews",
            "Чисто и вкусно",
            "Ресторан ещё не открылся",
            False,
        ),
        (
            "https://2gis.ru/ufa/inside/70030076353167626/query/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001082903174/tab/reviews",
            "Очень медленное обслуживание, ооооочень медленно",
            "Всё классно)) спасибо за открытие!",
            False,
        ),
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255/tab/reviews",
            "супер место",
            "Заказал с собой 3 гамбургера, картошку и чизбургер фреш. На месте не проверил",
            False,
        ),
        # Wrong url
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594",
            "Чисто и вкусно",
            "Ресторан ещё не открылся",
            True,
        ),
    ],
)
async def test_fetcher(url: str, plained_review: str, last_plained_review: str, fail: bool) -> None:
    """
    Тестирует fetcher на уже имеющихся на страницу комментариях.

    Args:
        url: url адрес ресторана
        plained_review: ожидаемый отзыв
        last_plained_review: последний ожидаемый отзыв (для проверки прокрутки отзывов)
        fail: должен ли провалиться тест

    """
    fetcher = HtmlFetcher(url)
    try:
        content = await fetcher.get_html_content()
        assert not fail
        assert plained_review in content
        assert last_plained_review in content
    except Exception:
        assert fail


@pytest.mark.parametrize(
    ("plained_review", "find"), [("Чисто и вкусно", True), ("Ресторан ещё не открылся", False)]
)
async def test_chunk_fetcher(plained_review: str, find: bool) -> None:
    """
    Тестирует частичную прогрузку отзывов.

    Args:
        plained_review: планируемый отзыв
        find: должен ли быть найден

    """
    fetcher = HtmlFetcher(TEST_URL)
    content = await fetcher.get_html_content(80)
    if plained_review in content:
        assert find
    else:
        assert not find
