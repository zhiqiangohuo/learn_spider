from django.urls import path

from .import views
# 这里注册URL
# ex: 
urlpatterns = [
    path('index', views.cbgnum,name='index'),
    path('find', views.getOrderinfo,name='find'),
    path('getmsg',views.returnmsg,name='returnmsg'),
    path('getmsg2',views.returnmsg2,name='returnmsg2')


]

