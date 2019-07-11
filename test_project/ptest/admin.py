from django.contrib import admin
from .models import Orderinfo,ReturnMessage,cbgspider
# Register your models here.
@admin.register(Orderinfo)
class OrderinfoAdmin(admin.ModelAdmin):
    list_display=('id','companyId','gasId','configId','startCountTime','isOiling')
@admin.register(ReturnMessage)
class ReturnMessageAdmin(admin.ModelAdmin):
    list_display=('returnCode','returnMsg','data')
@admin.register(cbgspider)
class cbgspiderAdmin(admin.ModelAdmin):
    list_display=('id','serverid','name','grade','leve', 'price','time_remain','purch_url')