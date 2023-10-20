from django.contrib import admin
from .models import * # 引入产品表

admin.site.register(Goods) # 注册产品表
admin.site.register(GoodsCategory) # 注册产品表