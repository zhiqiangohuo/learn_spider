import scrapy
import pickle
import json
from ..items import QidianItem
class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['qidian.com']
    start_urls = ['https://book.qidian.com/info/3676417']
    all_id = pickle.load(open("all_book_id.pkl",'rb'))
    start_urls = ['https://book.qidian.com/info/{}'.format(id) for id in all_id ]
    def parse(self, response):
        item = QidianItem()
        title = response.xpath("/html/body/div/div[6]/div[1]/div[2]/p[1]/a/text()").extract()
        pid = response.url.split("info/")[-1]
        tag = response.xpath("/html/body/div/div[6]/div[1]/div[2]/p[1]/a/text()").extract()  # 系统标签
        tags = response.xpath("/html/body/div/div[6]/div[4]/div[1]/div[1]/div[2]/ul/li[1]/div/p/a/text()").extract() # 作者自定义标签
        intro = response.xpath("/html/body/div/div[6]/div[4]/div[1]/div[1]/div[1]/p/text()").extract() # 介绍
        item["title"] = title
        item['tag'] = tag[0]
        item['bookId'] = pid
        item['tags'] = tags
        item['intro'] = intro
        yield item
