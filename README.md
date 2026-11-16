# Books Scraper

Собрает данные обо всех книгах каталога (название, цена, рейтинг,
количество в наличии, описание и характеристики из таблицы
Product Information) и сохранить их в текстовый файл. Сбор можно
запускать автоматически каждый день в 19:00.

## Структура проекта

```
books_scraper/
├── artifacts/
│   └── books_data.txt        # результат парсинга
├── notebooks/
│   └── HW_03_python_ds.ipynb
├── tests/
│   └── test_scraper.py       # автотесты на pytest
├── conftest.py               # настройка путей импорта для pytest
├── scraper.py                # основной скрипт
├── requirements.txt
└── README.md
```

## Установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск

Разовый сбор данных (файл `books_data.txt` появится в текущей папке):

```python
from scraper import scrape_books

scrape_books(is_save=True)
```

Ежедневный автоматический запуск в 19:00 (скрипт должен оставаться
запущенным; остановить можно через Ctrl+C):

```bash
python scraper.py
```

Время запуска меняется в вызове `run_scheduler(run_time="19:00")`
в конце `scraper.py`.

