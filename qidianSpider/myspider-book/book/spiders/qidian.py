import scrapy
from copy import deepcopy
from ..items import BookItem
import json
import requests
import random
from ..extraip import ExtraIp
class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com']
    start_urls = ['https://www.qidian.com/all?orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0']
    extr = ExtraIp()
    def parse(self, response):
        lis = response.xpath("//div[@class='work-filter type-filter']/ul/li")[1:]
        for i in lis:
            item = BookItem()
            # item["rtype"] = i.xpath("./a/text()").extract_first()
            type_url = "https://" + i.xpath("./a/@href").extract_first()
            # print("第一次跳转的URL",type_url)
            yield scrapy.Request(url=type_url, callback=self.parse_type, meta={"item": item}, dont_filter=True)

    def parse_type(self, response):

        item = response.meta["item"]
        lis = response.xpath("//div[@class='book-img-text']/ul/li")
        for i in lis:
            item["rurl"] = "https:" + i.xpath("./div[@class='book-img-box']/a/@href").extract_first()
            # item["rimg"] = "http:" + i.xpath("./div[@class='book-img-box']/a/img/@src").extract_first()
            # item["rtitle"] = i.xpath("./div[@class='book-mid-info']/h4/a/text()").extract_first()
            # item["rauthor"] = i.xpath("./div[@class='book-mid-info']/p[@class='author']/a[@class='name']/text()").extract_first()
            # item["rintro"] = i.xpath("./div[@class='book-mid-info']/p[@class='intro']/text()").extract_first()

            yield scrapy.Request(url=item["rurl"], callback=self.parse_detail, meta={"item": deepcopy(item)}, dont_filter=True)

        next_url = response.xpath("//div[@class='lbf-pagination']/ul/li/a[@class='lbf-pagination-next ']/@href").extract_first()

        if next_url != "javascript:;" and next_url is not None:
            next_url = "https:" + next_url
            yield scrapy.Request(url=next_url, callback=self.parse_type, meta={"item": deepcopy(item)}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta["item"]
        # item["rtag"] = response.xpath("//div[@class='book-info ']/p[@class='tag']/*/text() | //div[@class='detail']/p[@class='tag-wrap']/a/text()").extract()
        # item['rtag'] = str(item['rtag'])
        fansurl = "https://book.qidian.com/fansrank/"+item['rurl'].split("/")[-1]
        yield scrapy.Request(url=fansurl, callback=self.parse_fansrank, meta={"item": deepcopy(item)}, dont_filter=True)
        # yield item
    def parse_fansrank(self,response):
        """
        获取用户列表以及用户信息的URL
        https://my.qidian.com/user/365729144?targetTab=0
        """
        item = response.meta["item"]
        user_index_url = response.xpath("//*[@data-num='500']/div/ul/li/a/@href").extract()
        user_index_url = ["https:"+i for i in user_index_url]

        for url in user_index_url:
            yield scrapy.Request(url=url, callback=self.parse_fansindex, meta={"item": deepcopy(item)},
                                 dont_filter=True)

    def parse_fansindex(self,response):
        """
        url  “https://my.qidian.com/user/365729144?targetTab=0”
        请求用户详情页
        获取： 1. 性别，地区，关注量，收藏，订阅，打赏，书架藏书，
                订阅作品，投月票，投推荐票。
        :param response:
        :return:
        """
        item = response.meta['item']
        userinfo= response.xpath("//div[@class='header-msg-desc']/text()").extract()[0]
        rtitle = response.xpath("//div[@class='header-msg-title']/text()").extract()[0]
        item['rname'] = response.xpath("//*[@id='elUidWrap']/a[1]/text()").extract()[0]
        item['rwatch'] = response.xpath("//span[@class='mr8']/strong/text()").extract()[0]
        item['rfans'] = response.xpath("//span[@class='ml12 mr8']/strong/text()").extract()[0]
        userinfo = userinfo.replace(" ","").replace("xa0","").split("/")
        if len(userinfo)== 0:
            item['rsex'] = None
            item['location'] = None
        elif len(userinfo) == 1:
            item['rsex'] = userinfo[0].replace(" ","")
        elif len(userinfo) == 2:
            item['rsex'],item['location'] = userinfo[0].replace(" ",""),userinfo[1].replace(" ","").replace("xa0","")
        item['rtitle'] = rtitle.replace("称号: ", "")
        #  省市区没有划分

        # 收藏量
        item['userid'] = response.url.split("/")[-1]

        url = "https://my.qidian.com/ajax/User/FriendHistory?id={}".format(item['userid'])
        yield scrapy.Request(url=url, callback=self.parse_FriendHistory, meta={"item": deepcopy(item)},
                             dont_filter=True)
    def parse_FriendHistory(self,response):
        item = response.meta['item']
        data =response.text
        data = json.loads(data)
        if data['data'] != []:
            item.update(data['data']['historyData']) # 收藏，订阅，打赏，月票，推荐票
        for i in range(13):
            Flage =True
            url = "https://my.qidian.com/ajax/user/FriendFansList?&id={}&levelId={}".format(item['userid'], i)
            while Flage:
                ip = random.choice(self.extr.ippool)
                proxies = {
                    "https":ip
                }
                try:
                    print("当前使用IP{}".format(ip))
                    res = requests.get(url=url,proxies=proxies,timeout=3)
                    if res.status_code==200:
                        Flage = False
                    else:
                        raise print("反扒")
                except Exception as e:
                    print("错误",e)
                    Flage = True
                    self.extr.deletip(ip)
            print(res.status_code)
            data = json.loads(res.text)
            data = data['data']['books']
            item['level{}'.format(i)] = json.dumps(data, ensure_ascii=False)
            item['booklist{}'.format(i)] = str([line['bookId'] for line in data])
            item['booknamelist{}'.format(i)] = str([line['bookName'] for line in data])
            # yield scrapy.Request(url=url, callback=self.parse_FriendList, meta={"item":deepcopy(item)},
            #                      dont_filter=True)

            # item.update(pre
        yield item












