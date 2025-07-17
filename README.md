При сборке образа устанавливаются зависимости для **playwright**.
Команда для сборки образа:
`sudo docker build -t reviews_parser:latest .`

Все тесты лежат в директории tests. Есть unit тесты, и интеграционные тесты, которые требуют получения html страницы.
Команда для запуска тестов:
`sudo docker run -d -v ./reviews_db:/project/reviews_db reviews_parser:latest pytest`

Команда для запуска скрипта в фоновом режиме:
`sudo docker run -d -v ./reviews_db:/project/reviews_db reviews_parser:latest python -m source.main`
