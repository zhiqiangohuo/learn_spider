# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NshspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 服务器
    serverid = scrapy.Field()
    # 账号名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 等级
    leve = scrapy.Field()
    # 评分
    grade = scrapy.Field()
    # 剩余时间
    time_remain = scrapy.Field()
    # 购买链接
    purch_url = scrapy.Field()


