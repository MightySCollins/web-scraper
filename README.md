# Web Scraper
This is a rough draft and proof of concept for a web crawler using `Scrapy`. It is able to parse the 4chan site and get information for the latest threads. It is not perfect but demonstrates the simplicity.
Why 4Chan?
It has a fairly nice html syntax and was quite easy to parse as well as being image based

## Running the Crawler
Run the following commands if you have docker installed.
```bash
docker-compose up
docker-compose run scrapy bash
scrapy crawl fourchan_data -o data.json # The version with pure http requests
scrapy crawl fourchan # Uses Splash anc generates full page image
```

## Splash
Splash is what is used to render the Javascript and runs a service. It can be used to generate full page screen shots and click on Javascript elements. You can hit it on port 8050 to see a webui where you can test your Lua.

# Useful Links I used
- http://stackoverflow.com/questions/28852057/change-ip-address-dynamically
- https://github.com/aivarsk/scrapy-proxies
- http://multiproxy.org/txt_all/proxy.txt
- https://github.com/scrapy/scrapyd-client
- https://github.com/scrapy-plugins/scrapy-splash
- https://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash/
- https://github.com/scrapy/scrapy

## The scraper works do don't expect many changes
