import pytest

from source.url_normilizer import UrlNormilizer


@pytest.mark.parametrize(
    ("url", "plained_url", "reviews_endpoint"),
    [
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/tab/reviews?m=56.019974%2C54.607869%2F11",
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/tab/reviews?m=56.019974%2C54.607869%2F11",
            "/tab/reviews",
        ),
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/tab/reviews?m=56.019974%2C54.607869%2F11",
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594/page/tab/reviews",
            "/page/tab/reviews",
        ),
        (
            "https://2gis.ru/ufa/inside/70030076353167626/query/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001082903174/tab/reviews",
            "https://2gis.ru/ufa/inside/70030076353167626/query/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001082903174/tab/reviews",
            "/tab/reviews",
        ),
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255/tab",
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255/tab/reviews",
            "/tab/reviews",
        ),
        (
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255",
            "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255/tab/reviews",
            "/tab/reviews",
        ),
    ],
)
def test_normilizer(url: str, plained_url: str, reviews_endpoint: str) -> None:
    """
    Тестирует нормализацию url.

    Args:
        url: исходное url
        plained_url: ожидаемое url после нормализации
        reviews_endpoint: эндпоинт отзывов организации

    """
    normilizer = UrlNormilizer(reviews_endpoint)
    url = normilizer.normilize(url)
    assert url == plained_url
