#
#
# import requests
# from lxml import etree
#
# url = "https://my.qidian.com/user/305509501?targetTab=0"
# response = requests.request("GET", url,)
# html = etree.HTML(response.text)
# # print(html.xpath("//div[@class='header-msg-desc']/text()"))
# userinfo = html.xpath("//span[@class='ml12 mr8']/strong/text()")
#
# print(userinfo[0])
# # print(response.text)
# # s = "booknamelist{} = scrapy.Field()"
# # for i in range(13):
# #   print(s.format(i))
import requests, re
from fontTools.ttLib import TTFont
from io import BytesIO


def get_font(url):
    response = requests.get(url)
    font = TTFont(BytesIO(response.content))
    cmap = font.getBestCmap()
    font.close()
    return cmap


def get_encode(cmap, values):
    WORD_MAP = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                'eight': '8', 'nine': '9', 'period': '.'}
    word_count = ''
    list = values.split(';')
    list.pop(-1)
    for value in list:
        value = value[2:]
        key = cmap[int(value)]
        word_count += WORD_MAP[key]
    return word_count


def get_nums(url):
    # 获取当前页面的html
    response = requests.get(url).text
    print("response", response)
    # doc = pq(response)
    pattern = re.compile('</style><span.*?>(.*?)</span>', re.S)
    print("pattern", pattern)
    #  获取当前页面所有被加密的数字字符
    numberlist = re.findall(pattern, response)
    print("numberlist", numberlist)
    # 获取当前包含字体文件链接的文本
    reg = re.compile('<style>(.*?)\s*</style>', re.S)
    fonturl = re.findall(reg, response)[0]
    print("fonturl", fonturl)
    # 通过正则获取当前页面字体文件链接
    url = re.search('woff.*?url.*?\'(.+?)\'.*?truetype', fonturl).group(1)
    print("url", url)
    cmap = get_font(url)
    print('cmap:', cmap)
    num_list = []

    for a in numberlist:
        num_list.append(get_encode(cmap, a))
    return num_list


def main(url):  # 为外界提供一可以调取的接口
    num_list = get_nums(url)
    return num_list


if __name__ == '__main__':
    url = 'https://book.qidian.com/info/1024757253'
    num_list = main(url)
    print(num_list)