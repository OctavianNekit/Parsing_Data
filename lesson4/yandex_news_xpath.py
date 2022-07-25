from lxml import html
import requests as req
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['News']
collections = db.news_collection

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36'}

response = req.get("https://yandex.ru/news/", headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//div[@class = 'mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top']/div[contains(@class, 'mg-grid__col mg-grid__col_xs')]")
for item in items:
    name = item.xpath(".//a//h2[@class = 'mg-card__title']/text()")[0].replace('\xa0', " ")
    source = item.xpath(".//a[@class = 'mg-card__source-link']/text()")[0]
    link = item.xpath(".//a[@class = 'mg-card__link']/@href")[0]
    date = str(datetime.date.today())
    print(name, link, source, date)
    document = {'name': name,
                'date': date,
                'link': link,
                'source': source}
    db.news_yandex.insert_one(document)
