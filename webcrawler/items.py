# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def http(values):
    return ['http:%s' % value for value in values]


class PostItem(scrapy.Item):
    subject = scrapy.Field()
    author = scrapy.Field()
    message = scrapy.Field()
    image_urls = scrapy.Field(output_processor=http)
    images = scrapy.Field()
