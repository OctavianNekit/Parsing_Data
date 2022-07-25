# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramProjectItem(scrapy.Item):
    _id = scrapy.Field()
    id_user = scrapy.Field()
    follow_id = scrapy.Field()
    group = scrapy.Field()
    name = scrapy.Field()
    photo_url = scrapy.Field()
