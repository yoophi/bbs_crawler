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
    site = scrapy.Field()
    board = scrapy.Field()
    created_at = scrapy.Field()

    cnt_hit = scrapy.Field()
    cnt_vote = scrapy.Field()
    cnt_comment = scrapy.Field()
