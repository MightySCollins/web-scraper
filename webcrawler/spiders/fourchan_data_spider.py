import datetime
import base64
import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import TakeFirst
from scrapy.linkextractors import LinkExtractor

from webcrawler.items import PostItem


class FourChanSpider(CrawlSpider):
    name = "fourchan_data"
    allowed_domains = ['4chan.org']
    start_urls = ['http://boards.4chan.org/g/']

    rules = (
        # Rule(LinkExtractor(allow=('/g/'))),
        Rule(LinkExtractor(allow=('/g/thread/*')), callback='parse_thread'),
    )

    def parse_thread(self, response):
        for sel in response.xpath('//div[@class="post op"]'):
            l = ItemLoader(item=PostItem(), selector=sel)
            l.default_output_processor = TakeFirst()
            l.add_xpath('subject', './div[@class="postInfo desktop"]/span[@class="subject"]/text()')
            l.add_xpath('author', './div[@class="postInfo desktop"]/span[@class="nameBlock"]/span/text()') # WARNING this will not yet do mods...
            l.add_xpath('image_urls', './div[@class="file"]/div[@class="fileText"]/a/@href')
            l.add_xpath('message', './blockquote[@class="postMessage"]') # Still got the block quote in...
            yield l.load_item()
