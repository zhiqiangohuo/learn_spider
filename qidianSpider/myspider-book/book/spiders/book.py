import scrapy
from copy import deepcopy
from ..items import BookItem
import json
import requests
import requests, re
from fontTools.ttLib import TTFont
from io import BytesIO
class QidianSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['www.qidian.com']
    start_urls = ['https://www.qidian.com/all?orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0']

    def get_font(self, url):
        response = requests.get(url)
        font = TTFont(BytesIO(response.content))
        cmap = font.getBestCmap()
        font.close()
        return cmap

    def get_encode(self, cmap, values):
        WORD_MAP = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6',
                    'seven': '7',
                    'eight': '8', 'nine': '9', 'period': '.'}
        word_count = ''
        list = values.split(';')
        list.pop(-1)
        for value in list:
            value = value[2:]
            key = cmap[int(value)]
            word_count += WORD_MAP[key]
        return word_count
    def parse(self, response):
        lis = response.xpath("//div[@class='work-filter type-filter']/ul/li")[1:]
        for i in lis:
            item = BookItem()
            item["rtype"] = i.xpath("./a/text()").extract_first()
            type_url = "https://" + i.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=type_url, callback=self.parse_type, meta={"item": item}, dont_filter=True)

    def parse_type(self, response):

        item = response.meta["item"]
        lis = response.xpath("//div[@class='book-img-text']/ul/li")
        for i in lis:
            item["rurl"] = "https:" + i.xpath("./div[@class='book-img-box']/a/@href").extract_first()
            item["rimg"] = "http:" + i.xpath("./div[@class='book-img-box']/a/img/@src").extract_first()
            item["rtitle"] = i.xpath("./div[@class='book-mid-info']/h4/a/text()").extract_first()
            item["rauthor"] = i.xpath("./div[@class='book-mid-info']/p[@class='author']/a[@class='name']/text()").extract_first()
            item["rintro"] = i.xpath("./div[@class='book-mid-info']/p[@class='intro']/text()").extract_first()
            item['rintro']  =item['rintro'].replace("\r","").replace(" ","")
            yield scrapy.Request(url=item["rurl"], callback=self.parse_detail, meta={"item": deepcopy(item)}, dont_filter=True)

        next_url = response.xpath("//div[@class='lbf-pagination']/ul/li/a[@class='lbf-pagination-next ']/@href").extract_first()

        if next_url != "javascript:;" and next_url is not None:
            next_url = "https:" + next_url
            yield scrapy.Request(url=next_url, callback=self.parse_type, meta={"item": deepcopy(item)}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta["item"]
        item["rtag"] = response.xpath("//div[@class='book-info ']/p[@class='tag']/*/text() | //div[@class='detail']/p[@class='tag-wrap']/a/text()").extract()
        item['rtag'] = str(item['rtag'])
        # 作品字数，作品推荐数，作品月票数，周推荐，作品总数，累计字数，创作天数，
        item['countword'] = ""
        res = response.text
        pattern = re.compile('</style><span.*?>(.*?)</span>', re.S)
        numberlist = re.findall(pattern, res)
        reg = re.compile('<style>(.*?)\s*</style>', re.S)
        fonturl = re.findall(reg, res)[0]
        url = re.search('woff.*?url.*?\'(.+?)\'.*?truetype', fonturl).group(1)
        cmap = self.get_font(url)
        num_list = []
        for a in numberlist:
            num_list.append(self.get_encode(cmap, a))
        item['countword'] = num_list[0]
        item['totalrecomment'] = num_list[2]
        item['weekrecomment'] = num_list[3]
        item['totalbook'] = response.xpath("//ul[@class='work-state cf']/li[1]/em/text()").extract_first()
        item['totalword'] = response.xpath("//ul[@class='work-state cf']/li[2]/em/text()").extract_first()
        item['totalday'] = response.xpath("//ul[@class='work-state cf']/li[3]/em/text()").extract_first()
        yield item





