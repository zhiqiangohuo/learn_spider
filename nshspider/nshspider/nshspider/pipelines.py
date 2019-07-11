# -*- coding: utf-8 -*-
import json
import codecs
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NshspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('cbg.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class MysqlPipeline(object):

    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='127.0.0.1',port=3306, user='root', passwd='12345678', db='port_test',charset='utf8',use_unicode=True)  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")
 
    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into ptest_cbgspider(name, serverid, grade, leve, price,time_remain,purch_url) VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['name'], item['serverid'], item['grade'], item['leve'],
                                         item['price'],item['time_remain'],item['purch_url']))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()
 
    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()