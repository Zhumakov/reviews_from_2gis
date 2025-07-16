import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

from main import LOADING_WAIT


REVIEWS_CONTAINER_CSS_SELECTOR = "div._qvsf7z"


class HtmlFetcher:
    """Получает содержимое html страницы."""

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    def __init__(self, url: str) -> None:
        """Используется для получения html содержимого страницы."""
        self.url = url

    async def get_html_content(self) -> str:
        """
        Открывает ссылку на страницу с отзывами, прогружает все отзывы и возвращает html страницы.

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

            while True:
                reviews_container = driver.find_element(
                    By.CSS_SELECTOR, REVIEWS_CONTAINER_CSS_SELECTOR
                )

                height = reviews_container.get_property("scrollHeight")
                driver.execute_script(
                    "arguments[0].scrollIntoView()",
                    reviews_container.find_elements(By.CSS_SELECTOR, "div._1k5soqfl")[-1],
                )
                await asyncio.sleep(LOADING_WAIT)

                new_height = reviews_container.get_property("scrollHeight")
                if new_height == height:
                    break

            return driver.page_source
        finally:
            driver.quit()
