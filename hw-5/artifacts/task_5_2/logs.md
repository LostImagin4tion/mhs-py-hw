
# Logs

```bash
poetry run python task_5_2.py --city moscow --rooms 1 --max-price 50000 --max-pages 1 --interval 1
```

Результат:

```text
Starting Cian scrapper for moscow...
Interval: every 1 minutes
2026-01-09 23:31:37,662 - src.data.json_storage - INFO - Storage file not found: artifacts/task_5_2/properties.json
2026-01-09 23:31:37,664 - src.data.json_storage - INFO - Saved 0 properties to artifacts/task_5_2/properties.json
[2026-x01-09 23:31:37] Check #1
2026-01-09 23:31:37,692 - src.scraper.scrapper - INFO - Built search URL: https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000
2026-01-09 23:31:37,692 - src.scraper.scrapper - INFO - Scraping page 1: https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000
2026-01-09 23:31:39,485 - httpx - INFO - HTTP Request: GET https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000 "HTTP/1.1 200 OK"
2026-01-09 23:31:39,673 - src.scraper.parser - INFO - Found 28 cards with selector: [data-name='CardComponent']
2026-01-09 23:31:39,747 - src.scraper.parser - INFO - Parsed 28 properties from page
2026-01-09 23:31:39,828 - src.scraper.parser - INFO - Found 6 pages
2026-01-09 23:31:39,828 - src.scraper.scrapper - INFO - Found 28 properties on page 1
2026-01-09 23:31:39,829 - src.scraper.scrapper - INFO - Found 28 new properties
2026-01-09 23:31:39,830 - src.data.json_storage - INFO - Saved 28 properties to artifacts/task_5_2/properties.json
        Found 28 new properties!
                --> 1-комн. квартира, 32,4 м², 25/25 этаж | 5,000 рублей
                https://www.cian.ru/rent/flat/191071633/
                --> Живи лучше, чем дома. Бронируй!1-комн. апартаменты, 35 м², 11/14 этаж | 3,999 рублей
                https://www.cian.ru/rent/flat/310694561/
                --> 1-комн. квартира, 33 м², 5/5 этаж | 50,000 рублей
                https://www.cian.ru/rent/flat/325597263/
        ... and 25 more
        Total stored: 28 | New: 28
        Next check in 1 minutes...

[2026-x01-09 23:32:39] Check #2
2026-01-09 23:32:39,920 - src.scraper.scrapper - INFO - Built search URL: https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000
2026-01-09 23:32:39,920 - src.scraper.scrapper - INFO - Scraping page 1: https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000
2026-01-09 23:32:41,915 - httpx - INFO - HTTP Request: GET https://www.cian.ru/cat.php?deal_type=rent&offer_type=flat&engine_version=2&region=1&room1=1&maxprice=50000 "HTTP/1.1 200 OK"
2026-01-09 23:32:42,087 - src.scraper.parser - INFO - Found 28 cards with selector: [data-name='CardComponent']
2026-01-09 23:32:42,159 - src.scraper.parser - INFO - Parsed 28 properties from page
2026-01-09 23:32:42,238 - src.scraper.parser - INFO - Found 6 pages
2026-01-09 23:32:42,238 - src.scraper.scrapper - INFO - Found 28 properties on page 1
2026-01-09 23:32:42,240 - src.scraper.scrapper - INFO - Found 0 new properties
        No new properties found
        Total stored: 28 | New: 28
        Next check in 1 minutes...

^C
Shutting down...
Scrapper stopped. Total new properties found: 28
```
