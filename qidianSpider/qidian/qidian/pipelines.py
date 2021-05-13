# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class QidianPipeline:
    def __init__(self):
        self.f =  open("../data/data.json", 'a+')

    def process_item(self, item, spider):

        json.dump(dict(item), self.f, ensure_ascii=False)
        self.f.write("\n")
        return item

    def __delete__(self, instance):
        self.f.close()
