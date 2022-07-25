# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from random import randint

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class NewProjectPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.instrument_base

    def process_item(self, item, spider):
        collection = self.db.Leroy_Merlin_collections
        collection.insert_one(item)
        return item


class NewProject_Photos(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError:
                    print("Error!")

    def item_completed(self, results, item, info):
        item['photos'] = [value[1] for value in results if value[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        folder_name = str(item['name'])
        lst = request.url.split("/")
        name = str(lst[-1])
        return f"{folder_name}/" + name
