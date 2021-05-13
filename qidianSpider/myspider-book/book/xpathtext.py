
import requests
from lxml import etree
import json
# url = "https://book.qidian.com/info/1024757253"
# response = requests.request("GET", url,)
# html = etree.HTML(response.text)
# # print(html.xpath("//div[@class='header-msg-desc']/text()"))
# userinfo = html.xpath("//ul[@class='work-state cf']/li[1]/em/text()")
# print(userinfo)
url = "http://x.fanqieip.com/gip?getType=1&qty=10&port=1&time=1&city=0&format=2&ss=1%2C2%2C3%2C4&dt=1&css="
res = requests.get(url=url)
data = json.loads(res.text)
print(data)
data = data['data']
ip_pool = []
for i in data:
    sockt = str(i['ip'])+":"+str(i['port'])
    ip_pool.append(sockt)
import requests
import random
url = "https://my.qidian.com/user/355736444?targetTab=0"

for ip in ip_pool:
    proxies = {
        "https": ip
    }
    try:
        response = requests.get(url=url,proxies=proxies,timeout=5)
        print(response.text)
    except:
        print("删除ip",ip)
        # proxy.remove(ip)