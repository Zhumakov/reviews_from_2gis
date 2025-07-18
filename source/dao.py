import aiosqlite


TABLE_CREATE_QUERY = """
CREATE TABLE IF NOT EXISTS reviews (
    ordinal_number INTEGER NOT NULL,
    firm_id TEXT NOT NULL,
    username TEXT NOT NULL,
    date TEXT NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER NOT NULL,

    PRIMARY KEY (ordinal_number, firm_id),
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

    async def insert_review(self, review_data: dict, ordinal_numer: int, firm_id: str) -> None:
        """
        Вставляет в таблицу отзыв.

        Если у организации, находящейся на firm_url уже есть отзыв с таким порядковым номером,
        значит этот отзыв - дупликат.

        Args:
            review_data: данные об отзыве
            ordinal_numer: порядковый номер отзыва
            firm_id: id организации, на которую написан

        """
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                INSERT INTO reviews (ordinal_number, firm_id, username, date, review, rating)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    ordinal_numer,
                    firm_id,
                    review_data.get("username", ""),
                    review_data.get("date", ""),
                    review_data.get("review", ""),
                    review_data.get("rating", ""),
                ),
            )
            await db.commit()

    async def get_last_insert_review(self, firm_id: str) -> int:
        """
        Возвращает порядковый номер последнего сохраненного отзыва.

        Args:
            firm_id: id организации, для которой нужно найти отзыв

        Returns:
            порядковый номер последнего сохраненного отзыва

        """
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                """
                SELECT * FROM reviews
                WHERE firm_id = ?
                ORDER BY ordinal_number DESC
                LIMIT 1;
                """,
                (firm_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return 0
            return row[0]

    async def get_all_reviews_to_firm(self, firm_id: str) -> list[dict[str, str]]:
        """
        Возвращает список со всеми отзывами указанной организации.

        Args:
            firm_id: firm_id

        Returns:
            Список с отзывами в виде словарей

        """
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute(
                """
                SELECT * FROM reviews
                WHERE firm_id = ?
                ORDER BY ordinal_number;
                """,
                (firm_id,),
            )
            rows = await cursor.fetchall()
            reviews = []
            for row in rows:
                reviews.append({
                    "ordinal_number": row[0],
                    "username": row[2],
                    "date": row[3],
                    "review": row[4],
                    "rating": row[5],
                })

            return reviews
