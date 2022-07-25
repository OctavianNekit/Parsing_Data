from lxml import html
import requests as req
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['News']
collections = db.news_collection

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36'}

response = req.get("https://news.mail.ru/", headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//table[@class = 'daynews__inner']//td[@class = 'daynews__main'] | //table[@class = 'daynews__inner']//div[@class = 'daynews__item']")
for item in items:
    in_news_item = item.xpath(".//a//@href")[0]
    in_news_response = req.get(in_news_item, headers=headers)
    dom_in = html.fromstring(in_news_response.text)
    name = dom_in.xpath(".//h1/text()")[0]
    link = in_news_item
    source = dom_in.xpath(".//div[@class = 'breadcrumbs breadcrumbs_article js-ago-wrapper']//span[@class = 'link__text'][1]/text()")[0]
    date = str(datetime.date.today())
    print(name, link, source, date)
    document = {'name': name,
                'date': date,
                'link': link,
                'source': source}
    db.news_mail.insert_one(document)
