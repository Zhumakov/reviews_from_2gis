import asyncio
import sys

from source.main import REVIEWS_ENDPOINT, DB_PATH
from source.dao import ReviewsDAO
from source.url_normilizer import UrlNormilizer


async def main(firm_url: str) -> None:
    """
    Извлекает из базы данных все отзывы к указанной организации и записывает их в txt файл.

    Args:
        firm_url: ссылка на страницу с карточкой заведения

    """
    normilizer = UrlNormilizer(REVIEWS_ENDPOINT)
    _, firm_id = normilizer.normilize(firm_url)
    dao = ReviewsDAO(DB_PATH)
    reviews = await dao.get_all_reviews_to_firm(firm_id)

    with open("reviews.txt", "w", encoding="utf8") as file:
        for review in reviews:
            file.write(str(review.get("ordinal_number", "")) + "\n")
            file.write("Дата отзыва: " + review.get("date", "") + "\n")
            file.write("Имя: " + review.get("username", "") + "\n")
            file.write(review.get("review", "") + "\n")
            file.write("Оценка: " + str(review.get("rating", "")) + "\n")
            file.write("\n")


if __name__ == "__main__":
    firm_url = sys.argv[1]
    asyncio.run(main(firm_url))
