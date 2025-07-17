import aiosqlite


TABLE_CREATE_QUERY = """
CREATE TABLE IF NOT EXISTS reviews (
    ordinal_numer INTEGER NOT NULL,
    url TEXT NOT NULL,
    username TEXT NOT NULL,
    date TEXT NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER NOT NULL,

    PRIMARY KEY (ordinal_numer, url),
    CHECK (rating BETWEEN 1 AND 5)
);
"""


class ReviewsDAO:
    """Класс для работы с базой данных."""

    def __init__(self, db_name: str) -> None:
        """
        Создаёт объект для работы с базой данных.

        Args:
            db_name: имя базы данных

        """
        self.db_name = db_name

    async def setup_db(self) -> None:
        """Создаёт базу данных и таблицу с отзывами, если их нет."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(TABLE_CREATE_QUERY)
            await db.commit()

    async def delete_db(self) -> None:
        """Удаляет таблицу с отзывами."""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                DROP TABLE IF EXISTS reviews;
                """
            )
            await db.commit()

    async def insert_review(self, review_data: dict, ordinal_numer: int, firm_url: str) -> None:
        """
        Вставляет в таблицу отзыв.

        Если у организации, находящейся на firm_url уже есть отзыв с таким порядковым номером,
        значит этот отзыв - дупликат.

        Args:
            review_data: данные об отзыве
            ordinal_numer: порядковый номер отзыва
            firm_url: url организации, на которую написан отзыв

        """
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                INSERT INTO reviews (ordinal_numer, url, username, date, review, rating)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    ordinal_numer,
                    firm_url,
                    review_data.get("username", ""),
                    review_data.get("date", ""),
                    review_data.get("review", ""),
                    review_data.get("rating", ""),
                ),
            )
            await db.commit()
