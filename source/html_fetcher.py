import asyncio

from playwright.async_api import async_playwright


TAB_NAVIGATOR_CSS_SELECTOR = "div._qvsf7z"
REVIEW_CSS_SELECTOR = "div._1k5soqfl"
NUMBER_OF_REVIEWS_CSS_SELECTOR = "span._1xhlznaa"

LOADING_WAIT = 2


class FetcherError(Exception):
    """Ошибки при получении страницы с отзывами."""


class HtmlFetcher:
    """Получает содержимое html страницы."""

    def __init__(self, url: str) -> None:
        """Используется для получения html содержимого страницы."""
        self.url = url

    async def get_html_content(self, last_saved_comment: int = 0) -> str:
        """
        Открывает ссылку на страницу с отзывами, прогружает все новые отзывы и возвращает html.

        Прогружает только новые отзывы, появившиеся после последнего сохранненного

        Args:
            last_saved_comment: порядковый номер последнего сохранненного отзыва

        Returns:
            html страницы

        Raises:
            FetcherError: ошибка при получении страницы

        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                locale="ru-RU",
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()
            await page.goto(self.url)

            tab_navigator = page.locator(TAB_NAVIGATOR_CSS_SELECTOR)
            await tab_navigator.wait_for()

            reviews_count_text = await tab_navigator.locator(
                NUMBER_OF_REVIEWS_CSS_SELECTOR
            ).text_content()
            if reviews_count_text is None:
                err_msg = "Не найден контейнер с вкладками"
                raise FetcherError(err_msg)

            number_of_reviews = int(reviews_count_text.replace(" ", "").replace(" ", ""))

            number_of_cycles = round((number_of_reviews - last_saved_comment) / 50)
            for _ in range(number_of_cycles):
                review_containers = page.locator(REVIEW_CSS_SELECTOR)
                count = await review_containers.count()

                last_review = review_containers.nth(count - 1)
                await last_review.scroll_into_view_if_needed()
                await asyncio.sleep(LOADING_WAIT)

            content = await page.content()
            await browser.close()
            return content
