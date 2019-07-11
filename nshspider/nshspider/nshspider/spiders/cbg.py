# -*- coding: utf-8 -*-
import scrapy
import sys
import re
# 导入item
from nshspider.items import NshspiderItem
class CbgSpider(scrapy.Spider):
    """逆水寒角色信息爬取
    """
    name = 'cbg'
#    allowed_domains = ['https://n.cbg.163.com']
    start_urls = ['https://n.cbg.163.com/cbg/query.py?serverid=2&act=search_role',
    'https://n.cbg.163.com/cbg/query.py?serverid=1&act=search_role',
    'https://n.cbg.163.com/cbg/query.py?serverid=3&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=4&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=5&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=6&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=7&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=8&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=9&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=8&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=11&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=12&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=14&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=15&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=16&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=6&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=19&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=4&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=25&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=22&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=15&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=4&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=25&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=39&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=39&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=36&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=4&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=51&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=32&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=42&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=39&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=35&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=36&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=37&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=25&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=39&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=44&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=36&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=42&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=51&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=44&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=52&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=47&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=44&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=16&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=4&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=51&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=52&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=16&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=35&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=55&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=56&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=57&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=15&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=36&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=3&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=42&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=64&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=12&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=72&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=72&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=17&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=64&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=22&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=44&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=72&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=89&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=86&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=87&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=88&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=6&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=6&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=6&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=76&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=77&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=77&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=77&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=76&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=81&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=81&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=83&act=search_role', 'https://n.cbg.163.com/cbg/query.py?serverid=84&act=search_role'
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=False)
    def parse(self, response):
        role_list = response.xpath("//section[@class='goodsw']/table/tr")[1:]

        if len(response.xpath("//div[@class='paging']/a[@class='btn pading-btn pading-btn_next']/@href")):
            next_url = 'https://n.cbg.163.com'+response.xpath("//div[@class='paging']/a[@class='btn pading-btn pading-btn_next']/@href").extract()[0]
        else:
            next_url=None
        for role in role_list:
            # 创建item 字段对象，用来存储信息到数据库
            item = NshspiderItem()
            item['serverid'] = role.xpath('./@data-serverid').extract()[0]
            item['name']= role.xpath("./td[2]/text()").extract()[0].replace('\n','').replace(' ','')
            item['grade'] = role.xpath("./td[3]/span/text()").extract()[0].replace('\n','').replace(' ','').replace(',','')
            item['leve'] = role.xpath("./td[4]/text()").extract()[0].replace('\n','').replace(' ','')
            item['price'] = re.findall('(\d+)',role.xpath("./td[5]/script/text()").extract()[0])[0]
            item['time_remain'] = role.xpath("./td[7]/text()").extract()[0].replace('\n','').replace(' ','')
            item['purch_url'] = 'https://n.cbg.163.com' + role.xpath("./td[8]/a/@href").extract()[0]
            yield item

        if next_url is not None:
            url = next_url
            yield scrapy.Request(url,callback=self.parse) 