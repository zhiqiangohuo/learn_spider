# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import re

class BookPipeline:
    def process_item(self, item, spider):

        return item

    def process_content(self, content):
        content = re.sub(r" |\r", '', content)
        return content


class MysqlPipeline(object):
    """
    同步操作
    """

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='123456',
                                    database='qidianspider')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        # sql语句
        print("存入数据")
        item_len = len(list(item.keys()))
        keys = tuple(item.keys())
        str_keys = str(keys).replace("'","")
        s = ["%s" for i in range(len(item.keys()))]
        insert_sql = "insert into writerinfo{} VALUES{}".format(str_keys,tuple(item.values()))
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql)
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()

