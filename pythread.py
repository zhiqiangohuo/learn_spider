import threading
content = []
import requests
import time

class MyThread(threading.Thread):
        # 重写threading以获取线程执行完毕后获取的返回值
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        # 重写方法
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def get_text(i,a):
    # 爬虫发送请求获取数据并处理
    """

    :param i: 页码
    :param a: 没有用
    :return: 请求到的json数据
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        "Cookie": "iuuid=2E2E54C9DFA7A314152C83D9A8AB65EAED9362398A0EB825F49CC3C0A43E7655; cityname=%E6%88%90%E9%83%BD; _lxsdk_cuid=16d43d6cfa9c8-0385ae9f8c816b-67e153a-144000-16d43d6cfa932; _lxsdk=2E2E54C9DFA7A314152C83D9A8AB65EAED9362398A0EB825F49CC3C0A43E7655; webp=1; i_extend=H__a100040__b1; ci=59; rvct=59%2C1167%2C646%2C647; _hc.v=c4dd75e2-5b94-ec18-87e0-d063f99a4312.1570853269; client-id=37208fbf-f55d-4cc5-ba15-a2de479334a7; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1572192891; __utma=211559370.1754194501.1572192892.1572192892.1572192892.1; __utmz=211559370.1572192892.1.1.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=zt_search; uuid=cda0d95991134777a94a.1572253882.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=45471131.1568880638007.1572187898426.1572253883194.14; _lxsdk_s=16e11a258f1-871-5a5-bb3%7C%7C24"
    }
    url = "https://cd.meituan.com/meishi/pn{}/".format(i)
    try:
        response = requests.get(url=url, headers=headers)
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding
        html_txt = response.text
        if response.status_code != 200:
            return None
        return html_txt
    except Exception as e:
        print("error", str(e))
def get_data(page_num):
    """
    创建线程
    :pagenum 页码数
    :return:
    """
    content = []
    st = time.time()
    li = []
    for i in range(page_num):
    #     print(i)
        #按照页码数创建线程
        t = MyThread(get_text,args=(i,i))
        li.append(t)
        t.start()
    # print(threading.enumerate())
    for t in li:
        t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
        content.append(t.get_result())

    et = time.time()
    print (et - st)
    return content
if __name__ == '__main__':
    get_data()