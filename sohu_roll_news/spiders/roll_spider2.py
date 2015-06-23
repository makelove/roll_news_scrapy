import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from sohu_roll_news.items import LinkItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import  Rule
from scrapy import log
from scrapy import Request

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

#from scrapy.log import start
#scrapy.log.start(logfile = 'log/spider.log',loglevel = 'INFO',logstdout = False)
import logging
#from scrapy.utils.log import configure_logging

#configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.ERROR
)

class rollspider2(Spider):

    def __init__(self):
        self.url_list = set()
    
    name="sohu_roll2"
    allowed_domains=["roll.sohu.com"]
    start_urls=["http://roll.sohu.com/index.shtml"]
    #url_list = set()
    
 
    def parse(self,response):
        sel=Selector(response)
        sites=sel.xpath('//div[@class="list14"]/ul/li')  
      
        for site in sites: 
            item = LinkItem() 
            item['title'] = site.xpath('a/text()').extract()  
            item['link'] = site.xpath('a/@href').extract()  
            item['type'] = site.xpath('em/a/text()').extract() 
            item['time'] = site.xpath('span/text()').extract()  
            yield item 
           
           
        nextpage=sel.xpath('//div[@class="pages"]/table/tr/td/a/@href').extract()
        for url in nextpage:
            url=url.replace("\n","")
            #print "url=",url
            
            if len(self.url_list) > 1000:
                break
            if url not in self.url_list:
                self.logger.error(url)
                self.url_list.add(url)
                yield Request(url, callback=self.parse)
