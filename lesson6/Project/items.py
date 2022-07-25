# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    _id = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    price_sale = scrapy.Field()
    price_not_sale = scrapy.Field()
    rate = scrapy.Field()
    link = scrapy.Field()
