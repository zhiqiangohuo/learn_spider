
import json
import requests


class ExtraIp():
    def __init__(self):
        self.url = "http://x.fanqieip.com/gip?getType=1&qty=40&port=1&time=1&city=0&format=2&dt=1&css="
        self.ippool = []
        self.ippool = self.get_ip_pool()
    def get_ip_pool(self):
        res = requests.get(url=self.url)
        data = json.loads(res.text)
        data = data['data']
        ip_pool = []
        for i in data:
            sockt = str(i['ip']) + ":" + str(i['port'])
            ip_pool.append(sockt)
        self.ippool.extend(ip_pool)
        return ip_pool
    def deletip(self,ip):

        self.ippool.remove(ip)
        if len(self.ippool)==0:
            # print("更新ip池")
            self.ippool = self.get_ip_pool()
