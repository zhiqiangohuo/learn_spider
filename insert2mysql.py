# 链接数据库

import pymysql
# from pymysql import escape_string, escape_dict


# 执行sql语句
data = {'poiId': 1469630,
        'frontImg': 'http://p0.meituan.net/600.600/mogu/d31aa6ccefa9ec1f4713acbe8402cc62204340.jpg',
        'title': '加豪加牛排（百伦店）',
        'avgScore': '3.5',
        'allCommentNum': '2020',
        'address': '百伦广场下沉式广场2号',
        'avgPrice': '54',
        'dealList': [],
        'hasAds': False,
        'adsClickUrl': '',
        'adsShowUrl': ""}
data['dealList'] = str(data['dealList'])

class Write2mysql():
    # def __init__(self,):
    #     self.connect = pymysql.connect(host="", user="root", password="12345678", db="qt_spider", charset="utf8")
    #     self.cur = self.connect.cursor()
    #     print("数据库连接成功")
    # def processitem(self,data):
    #     try:
    #
    #         sql = "insert into meituan(poiId,frontImg,title,avgScore,allCommentNum,address,avgPrice,dealList,hasAds,adsClickUrl,adsShowUrl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #
    #         value = [v for k, v in data.items()]
    #
    #         print(value)
    #         self.cur.execute(sql, tuple(value))
    #         # 事物提交
    #         self.connect.commit()
    #         print("插入数据库成功")
    #     except Exception as err:
    #         print("sql语句执行错误", err)
    #         self.connect.rollback()
    pass
