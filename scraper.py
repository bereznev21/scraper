import time
import requests
import schedule
from bs4 import BeautifulSoup
import re

def get_book_data(book_url: str) -> dict:
    """
    Собирает данные о книге со страницы каталога Books to Scrape.

    Функция загружает страницу книги, разбирает HTML и извлекает название,
    цену, рейтинг, количество в наличии, описание и все характеристики
    из таблицы Product Information.

    Args:
        book_url (str): Ссылка на страницу книги, например
            'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'.

    Returns:
        dict: Словарь с данными о книге:
            - "Название" (str): название книги;
            - "Цена" (float): цена в фунтах;
            - "Рейтинг" (int): рейтинг от 0 до 5;
            - "Количество в наличии" (int): число экземпляров на складе;
            - "Описание" (str | None): описание книги, если оно есть;
            - "Дополнительные характеристики" (dict): строки таблицы
              Product Information в виде «название: значение».
            Если сервер вернул код ответа, отличный от 200, возвращается
            пустой словарь.
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    rating = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    response = requests.get(book_url, timeout=15)
    response.encoding = "utf-8"
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        book_info = dict()
        html_text1 = soup.find(attrs={"class": "product_main"})
        book_name = html_text1.find("h1").get_text()
        book_price = html_text1.find(attrs={"class": "price_color"}).get_text()
        book_rate = html_text1.find(attrs={"class": "star-rating"})['class'][1]
        book_count = html_text1.find(attrs={"class": "instock availability"}).get_text().strip()
        description_header = soup.find(id="product_description")
        book_description = None
        if description_header is not None:
            book_description = description_header.find_next_sibling("p").get_text(strip=True)
        html2_text = soup.find(attrs={"class": "table table-striped"})
        book_info["Название"] = book_name
        book_info["Цена"] = float(re.search(r"\d+(?:\.\d+)?", book_price).group())
        book_info["Рейтинг"] = rating[book_rate]
        book_info["Количество в наличии"] = int(re.search(r'\d+', book_count).group(0))
        book_info["Описание"] = book_description
        add_spec = dict()
        for row in html2_text.find_all("tr"):
            name = row.find("th").get_text()
            value = row.find("td").get_text()

            if name == "UPC":
                add_spec["Универсальный код продукта"] = value
            elif name == "Product Type":
                add_spec["Тип продукта"] = value
            elif name == "Price (excl. tax)":
                add_spec["Цена без налога"] = float(re.search(r"\d+(?:\.\d+)?", value).group())
            elif name == "Price (incl. tax)":
                add_spec["Цена с налогом"] = float(re.search(r"\d+(?:\.\d+)?", value).group())
            elif name == "Tax":
                add_spec["Налог"] = float(re.search(r"\d+(?:\.\d+)?", value).group())
            elif name == "Availability":
                add_spec["Количество в наличии"] = int(re.search(r'\d+', value).group(0))
            elif name == "Number of reviews":
                add_spec["Количество отзывов"] = value
            
        book_info["Дополнительные характеристики"] = add_spec
        return book_info
    else:
        return(dict())


def scrape_books(is_save=False):
    """
    Собирает данные обо всех книгах каталога Books to Scrape.

    Функция последовательно обходит страницы каталога, собирает ссылки
    на книги, для каждой вызывает get_book_data и при необходимости
    сохраняет результат в файл.

    Args:
        is_save (bool): Если True, результат сохраняется в файл
            books_data.txt: по одному словарю с данными о книге
            на каждой строке. По умолчанию False.

    Returns:
        str: строка, которая содержит данные о книгах (формат описан
            в get_book_data). Страницы каталога, которые не удалось
            загрузить, пропускаются.
    """

    max_page = 50
    books = ""

    for page_number in range(1, max_page + 1):
        catalog_url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"
        response = requests.get(catalog_url, timeout=10)
        response.encoding = "utf-8"
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for article in soup.find_all("article", class_="product_pod"):
            link = article.find("h3").find("a")["href"]
            book_data = get_book_data("http://books.toscrape.com/catalogue/" + link)
            if book_data:
                books += str(book_data) + '\n'

    if is_save:
        with open("books_data.txt", "w", encoding="utf-8") as f:
            f.write(books)

    return books
