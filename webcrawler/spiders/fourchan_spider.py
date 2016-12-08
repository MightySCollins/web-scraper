import datetime
import base64
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy_splash import SplashRequest

from webcrawler.items import PostItem

script = """
-- Arguments:
-- * url - URL to render;
-- * css - CSS selector to render;
-- * pad - screenshot padding size.

-- this function adds padding around region
function pad(r, pad)
  return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
end

-- main script
function main(splash)

  -- this function returns element bounding box
  local get_bbox = splash:jsfunc([[
    function(css) {
      var el = document.querySelector(css);
      var r = el.getBoundingClientRect();
      return [r.left, r.top, r.right, r.bottom];
    }
  ]])

  assert(splash:go(splash.args.url))
  assert(splash:wait(0.5))

  -- don't crop image by a viewport
  splash:set_viewport_full()

  local region = pad(get_bbox(splash.args.css), splash.args.pad)
  return splash:png{region=region}
end
"""


class FourChanSpider(scrapy.Spider):
    name = "fourchan"
    start_urls = ['http://boards.4chan.org/g/']

    def start_requests(self):
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
            'wait': 1
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.json',
                                args=splash_args)

    def parse(self, response):
        png_bytes = base64.b64decode(response.data['png'])
        with open('images/pages/%s.png' % datetime.datetime.now(), 'wb') as f:
            f.write(png_bytes)

        for sel in response.xpath('//div[@class="post op"]'):
            l = ItemLoader(item=PostItem(), selector=sel)
            l.default_output_processor = TakeFirst()
            l.add_xpath('subject', './div[@class="postInfo desktop"]/span[@class="subject"]/text()')
            l.add_xpath('author', './div[@class="postInfo desktop"]/span[@class="nameBlock"]/span/text()') # WARNING this will not yet do mods...
            l.add_xpath('image_urls', '//div[@class="post op"]/div[@class="file"]/a[@class="fileThumb"]/img//@src')
            l.add_xpath('message', './blockquote[@class="postMessage"]') # Still got the block quote in...
            yield l.load_item()

