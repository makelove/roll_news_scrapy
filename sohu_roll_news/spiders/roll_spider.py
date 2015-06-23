from scrapy.spider import Spider
from scrapy.selector import Selector
from sohu_roll_news.items import LinkItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import  Rule

class rollspider(Spider):
    name="sohu_roll"
    allowed_domains=["roll.sohu.com"]
    start_urls=["http://roll.sohu.com/index.shtml"]
    
    def parse(self,response):
        sel=Selector(response)
        sites=sel.xpath('//div[@class="list14"]/ul/li')  
        
        items = []  
        for site in sites:  
            item = LinkItem()  
            item['title'] = site.xpath('a/text()').extract()  
            item['link'] = site.xpath('a/@href').extract()  
            item['type'] = site.xpath('em/a/text()').extract() 
            item['time'] = site.xpath('span/text()').extract()  
            items.append(item)  
        return items  
        
