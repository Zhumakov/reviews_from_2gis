При сборке образа устанавливаются зависимости для **playwright**.
Команда для сборки образа:

`sudo docker build -t reviews_parser:latest .`

Все тесты лежат в директории tests. Есть unit тесты, и интеграционные тесты, которые требуют получения html страницы.
Команда для запуска тестов:

`sudo docker run -d -v ./reviews_db:/project/reviews_db --rm reviews_parser:latest pytest`

Команда для запуска скрипта в фоновом режиме:

`sudo docker run -d -v ./reviews_db:/project/reviews_db --rm reviews_parser:latest python -m source.main`

Все отзывы сохраняются в базе данных sqlite3 по пути reviews_db/reviews.db

Чтобы настроить cron для ежедневного запуска, можно создать файл комманду с запуском скрипта:

`echo sudo docker run -d -v ./reviews_db:/project/reviews_db --rm reviews_parser:latest python -m source.main > command.sh`

Выдать ей права на исполнение:

`chmod +x command.sh`

Открыть редактор команд:

`crontab -e`

И ввести в строке:

`0 3 * * * /path/to/reviews_from_2gis/command.sh >> /path/to/reviews_from_2gis/cron_logs.txt`

Где `/path/to/reviews_from_2gis` - путь по которому лежит директория с парсером

Есть отдельный скрипт для получения отзывов из базы данных, он создаёт файл reviews.txt с отзывами,
в качестве аргумента нужно передать url указывающий на карточку организации в 2GIS.
Шаблон:

`python -m sorce.get_all_reviews <URL>`

Например:

`python -m source.get_all_reviews https://2gis.ru/ufa/search/%D0%B2%D0%BA%D1%83%D1%81%D0%BD%D0%BE%20%D0%B8%20%D1%82%D0%BE%D1%87%D0%BA%D0%B0/firm/70000001057550594`
