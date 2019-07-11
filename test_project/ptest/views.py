from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.http import request
import json
from rest_framework import viewsets
from .models import Orderinfo,ReturnMessage,cbgspider
from .serializer import UserSerializer,GroupSerializer,MessageSerializer
from django.contrib.auth.models import User,Group
import hashlib
import datetime
# 搭建服务端 伪造接口请求
def index(request):
    context = {"a":1,"b":2,"c":3}
    # JSON dumps 把字典类型转为JSON类型
    # JSON loads 把JSON类型转为字典类型
    text = "helloword"
    hl = hashlib.md5()
    text = hl.update(text.encode())
    print(text)
    return HttpResponse(text)
# Create your views here.
def getOrderinfo(request):
    context = {"a":1,"b":2,"c":3}
    # JSON dumps 把字典类型转为JSON类型
    # JSON loads 把JSON类型转为字典类型
    text = json.dumps(context)
    hl = hashlib.md5()
    hl.update(text.encode())
    print(text)
    return HttpResponse(hl.hexdigest())
def cbgnum(request):
    account = cbgspider.objects.filter(grade__gt=90000).order_by('price')
    content =[]   
    for msg in account:
        #print(type(msg.grade))
        if msg not in content:
            context = {
                '价格':msg.price,
                '评分':msg.grade,
                '用户名':msg.name,
                '购买链接':msg.purch_url

            }
            content.append(context)
    return HttpResponse(json.dumps(content,ensure_ascii=False))
def returnmsg(request):
    msg = ReturnMessage.objects.filter(id=1)[0]
    context = {}
    if msg is not None :
        context.update({"status":"succed"})
        json_msg ={
            'rcode':msg.returnCode,
            'rmsg':msg.returnMsg,
            'data':msg.data,
            'data':str(datetime.datetime.now())
        }

        context.update({"data":json_msg})
        return HttpResponse(json.dumps(context,ensure_ascii=False,sort_keys=True,indent=4,separators=(',',':')),content_type="application/json")
def returnmsg2(request):
    a = 'error'
    b = 'lisi'
    c = 'wangwu'
    msg = {
        '1':a,
        '2':b,
        '3':c,
    }
    return HttpResponse(json.dumps(msg,ensure_ascii=False))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-data_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
class MessgViewSet(viewsets.ModelViewSet):
    queryset = ReturnMessage.objects.all()
    serializer_class = MessageSerializer
