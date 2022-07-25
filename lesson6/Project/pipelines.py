# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient


class ProjectPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.books_base

    def process_item(self, item, spider):
        def cleaner_html(dirty):
            cleaner = re.compile('<.*?>')
            clean_text = re.sub(cleaner, '', dirty)
            return clean_text

        if spider.name == 'book24':
            collection = self.db[spider.name]
            collection.insert_one(item)
        else:
            dirty_text = [item['author'], item['name'], item['price_sale'], item['price_not_sale'], item['rate'],
                      item['link']]
            data = []
            for field in dirty_text:
                if field is not None:
                    new_field = cleaner_html(field)
                    data.append(new_field)
                else:
                    data.append(field)
            finish_info = {"author": data[0], "name": data[1], "price_sale": data[2], "price_not_sale": data[3],
                           "rate": data[4], "link": data[5]}
            collection = self.db[spider.name]
            collection.insert_one(finish_info)
            return item
