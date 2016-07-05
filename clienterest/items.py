# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClienterestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()

    created_at = scrapy.Field()
    hit_cnt = scrapy.Field()
    vote_cnt = scrapy.Field()
