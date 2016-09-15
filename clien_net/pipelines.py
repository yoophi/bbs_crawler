# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class ClienterestPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'clien_net')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        _pk = {'site': item['site'], 'board': item['board'], 'id': item['id']}
        _meta_info = {k: item[k] for k in item.keys() if k.startswith('cnt_')}
        _meta_info['created_at'] = datetime.now()

        if self.collection.find_one(_pk):
            self.collection.update_one(_pk, {'$set': dict(item), '$push': {'meta_info': _meta_info}})
        else:
            self.collection.insert(dict(meta_info=[_meta_info], **dict(item)))

        return item


class RPMongoPipeline(object):
    """
    https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/
    """

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)

        return item
