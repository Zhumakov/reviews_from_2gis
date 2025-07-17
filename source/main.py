import asyncio
import os


from source.html_fetcher import HtmlFetcher
from source.parser import ReviewesParser
from source.url_normilizer import UrlNormilizer
from source.dao import ReviewsDAO


DB_PATH = "reviews_db/reviews.db"
REVIEWS_ENDPOINT = "/tab/reviews"
BRANCH_URLS = [
    "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594",
    "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001082903174",
    "https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/2393066583119255",
]


async def parsing_url(
    url: str, firm_id: str, last_saved_review: int
) -> tuple[list[dict[str, str]], str]:
    """
    Скачивает html страницу с отзывами и парсит её.

    Args:
        url: url страницы с отзывами
        last_saved_review: последний сохраненный отзыв организации
        firm_id: id организации

    Returns:
        Список отзывов, id организации

    """
    html_page = await HtmlFetcher(url).get_html_content(last_saved_review)
    return ReviewesParser(html_page).get_rewiews(last_saved_review), firm_id


async def main() -> None:
    if (additional_urls := os.getenv("BRANCH_URLS", None)) is not None:
        BRANCH_URLS.extend(additional_urls.split(","))

    if (new_reviews_endpoint := os.getenv("REVIEWS_ENDPOINT", None)) is not None:
        global REVIEWS_ENDPOINT
        REVIEWS_ENDPOINT = new_reviews_endpoint

    if (new_loading_wait := os.getenv("LOADING_WAIT", None)) is not None:
        global LOADING_WAIT
        LOADING_WAIT = float(new_loading_wait)

    # Инициализация базы данных
    reviews_dao = ReviewsDAO(DB_PATH)
    await reviews_dao.setup_db()

    # Нормализация эндпоинтов
    normilizer = UrlNormilizer(REVIEWS_ENDPOINT)
    urls_data = [normilizer.normilize(url) for url in BRANCH_URLS]

    # Получение последних сохраненных отзывов соответствующей организации
    last_saved_review = [
        await reviews_dao.get_last_insert_review(urls_data[i].firm_id)
        for i in range(len(urls_data))
    ]

    # Постановка асинхронных задач на парсинг страниц
    tasks = [
        parsing_url(urls_data[i].reviews_url, urls_data[i].firm_id, last_saved_review[i])
        for i in range(len(urls_data))
    ]
    pending = list(asyncio.as_completed(tasks))

    while pending:
        done_taks = pending.pop(0)
        # Ожидание выполнения задачи
        reviews, firm_id = await done_taks

        # Считывание отзывов с конца
        reviews.reverse()
        for ordinal_number, review_data in enumerate(reviews, start=1):
            await reviews_dao.insert_review(review_data, ordinal_number, firm_id)


if __name__ == "__main__":
    asyncio.run(main())
