import asyncio
import os


import html_fetcher
from parser import ReviewesParser
from url_normilizer import UrlNormilizer


REVIEWS_ENDPOINT = "/tab/reviews"
LOADING_WAIT = 2
BRANCH_URLS = [
    "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594",
    "https://2gis.ru/ufa/inside/70030076353167626/query/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001082903174",
    "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255",
]


async def parsing_url(url: str) -> list[dict[str, str]]:
    """
    Скачивает html страницу с отзывами и парсит её.

    Args:
        url: url страницы с отзывами

    Returns:
        Список отзывов

    """
    print("Task start")
    html_page = await html_fetcher.HtmlFetcher(url).get_html_content()
    return ReviewesParser(html_page).get_rewiews()


async def main() -> None:
    if (additional_urls := os.getenv("BRANCH_URLS", None)) is not None:
        BRANCH_URLS.extend(additional_urls.split(","))

    if (new_reviews_endpoint := os.getenv("REVIEWS_ENDPOINT", None)) is not None:
        global REVIEWS_ENDPOINT
        REVIEWS_ENDPOINT = new_reviews_endpoint

    if (new_loading_wait := os.getenv("LOADING_WAIT", None)) is not None:
        global LOADING_WAIT
        LOADING_WAIT = float(new_loading_wait)

    normilizer = UrlNormilizer(REVIEWS_ENDPOINT)
    urls = [normilizer.normilize(url) for url in BRANCH_URLS]

    tasks = [parsing_url(url) for url in urls]
    pending = list(asyncio.as_completed(tasks))

    while pending:
        done_taks = pending.pop(0)
        reviews = await done_taks
        for review in reviews:
            for field in review.values():
                print(field)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
