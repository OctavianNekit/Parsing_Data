from lxml import html
import requests as req
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['News']
collections = db.news_collection

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36'}

response = req.get("https://lenta.ru/", headers=headers)
dom = html.fromstring(response.text)
source = "https://lenta.ru/"

items = dom.xpath("//div[@class = 'span4']/div[@class = 'item']")
for item in items:
    name = item.xpath(".//a/text()")[0].replace("\xa0", " ")
    link = source + item.xpath(".//a/@href")[0]
    date = item.xpath(".//time/@title")[0]
    print(name, link, date)
    document = {'name': name,
                'date': date,
                'link': link,
                'source': source}
    db.news_lenta.insert_one(document)

