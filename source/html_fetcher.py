import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth


TAB_NAVIGATOR_CSS_SELECTOR = "div._qvsf7z"
REVIEW_CSS_SELECTOR = "div._1k5soqfl"
NUMBER_OF_REVIEWS_CSS_SELECTOR = "span._1xhlznaa"

LOADING_WAIT = 2


class HtmlFetcher:
    """Получает содержимое html страницы."""

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

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

        """
        driver = webdriver.Chrome(options=self.chrome_options)
        stealth(
            driver,
            languages=["ru-RU", "ru"],
            platform="Linux x86_64",
            webgl_vendor="Intel Inc.",
            renderer="Mesa DRI Interl(R) UHD Graphics 620 (Kabylake GT2)",
            fix_hairline=True,
        )
        try:
            driver.get(self.url)
            await asyncio.sleep(LOADING_WAIT + 2)

            tab_navigator = driver.find_element(By.CSS_SELECTOR, TAB_NAVIGATOR_CSS_SELECTOR)
            number_of_reviews = int(
                tab_navigator.find_element(By.CSS_SELECTOR, NUMBER_OF_REVIEWS_CSS_SELECTOR).text
            )

            number_of_cycles = round((number_of_reviews - last_saved_comment) / 50)
            for _ in range(number_of_cycles):
                driver.execute_script(
                    "arguments[0].scrollIntoView()",
                    tab_navigator.find_elements(
                        By.CSS_SELECTOR,
                        REVIEW_CSS_SELECTOR,
                    )[-1],
                )
                await asyncio.sleep(LOADING_WAIT)

            return driver.page_source
        finally:
            driver.quit()
