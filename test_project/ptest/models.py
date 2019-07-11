from django.db import models
from django.utils import timezone
# 这里创建数据库
class Orderinfo(models.Model):
    # 运营商id
    companyId = models.CharField(max_length=200,verbose_name='运营商id')
    # 加油站id
    gasId = models.CharField(max_length=200,verbose_name='加油站id')
    # 活动id
    configId = models.CharField(max_length=200,verbose_name='活动id')
    # 运营商
    # companyName = models.CharField(max_length=200)
    # 开始统计时间
    startCountTime = models.DateField(verbose_name='开始时间')
    startCountTime = models.DateField(verbose_name='结束时间')
    isOiling = models.BooleanField(default=True,verbose_name='是否加油')
    class Meta:
        verbose_name = "加油信息查询"
        verbose_name_plural = "加油站信息"

class ReturnMessage(models.Model):
    returnCode = models.CharField(max_length=200,verbose_name='状态码返回')
    returnMsg = models.CharField(max_length=200,verbose_name='返回消息')
    data = models.CharField(max_length=200,verbose_name='返回数据')
    class Meta:
        verbose_name = '接口返回信息'
        verbose_name_plural = '接口返回信息'
class credit_user(models.Model):
    pripid = models.CharField(max_length=200,verbose_name ='PRIPID' )
    creditnum=models.CharField(max_length=200,verbose_name ='统一社会信用代码')
    regnum = models.CharField(max_length=200,verbose_name='注册号')
    companyname = models.CharField(max_length=200,verbose_name='公司名称')
    typenum= models.CharField(max_length=200,verbose_name='类型编号')
    typename = models.CharField(max_length=200,verbose_name='类型名称')
    liaison =  models.CharField(max_length=200,verbose_name='联络员')
    licardid= models.CharField(max_length=200,verbose_name='联络员证件号')
    liphone=models.CharField(max_length=200,verbose_name='联络员手机号')
    class Meta:
        verbose_name = '工商系统登录账号'
        verbose_name_plural="工商账号"
class cbgspider(models.Model):
    serverid = models.CharField(max_length=200,verbose_name ='服务器id' )
    name = models.CharField(max_length=200,verbose_name ='用户名')
    grade = models.IntegerField(max_length=200,verbose_name='评分')
    leve = models.CharField(max_length=200,verbose_name='等级')
    price = models.IntegerField(max_length=200,verbose_name='价格')
    time_remain = models.CharField(max_length=200,verbose_name='剩余时间')
    purch_url =  models.CharField(max_length=200,verbose_name='购买链接')
    # stunn = models.CharField(max_length=200,verbose_name='绝技')
    # rare = models.CharField(max_length=200,verbose_name='词条')
    # clothes = models.CharField(max_length=200,verbose_name='衣品')
    # hourse = models.CharField(max_length=200,verbose_name='骏马值')
    class Meta:
        verbose_name = '逆水寒账号信息'
        verbose_name_plural="逆水寒账号"
    