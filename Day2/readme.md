# Task 2
## 创建数据表
在model.py中创建两个表：产品分类表和产品信息表。

```python
from django.db.models import *


# 产品分类表
class GoodsCategory(Model):
    name = CharField(max_length=64, verbose_name='名称')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')

## 产品表
class Goods(Model):
    """产品"""

    # 外键
    category = ForeignKey(GoodsCategory, on_delete=SET_NULL, related_name='goods_set', null=True, verbose_name='产品分类',
                          blank=True, )
    # on_delete 

    number = CharField(max_length=32, verbose_name='产品编号')
    name = CharField(max_length=64, verbose_name='产品名称')
    barcode = CharField(max_length=32, null=True, blank=True, verbose_name='条码')
    spec = CharField(max_length=64, null=True, blank=True, verbose_name='规格')
    shelf_life_days = IntegerField(null=True, verbose_name='保质期天数')
    purchase_price = FloatField(default=0, verbose_name='采购价')
    retail_price = FloatField(default=0, verbose_name='零售价')
    remark = CharField(max_length=128, null=True, blank=True, verbose_name='备注')
```

## 合并数据库
这两个命令在Django框架中扮演着至关重要的角色，用于执行数据库迁移操作。

```python
python manage.py makemigrations
```
这个命令的责任是生成迁移脚本。一旦你在Django模型中做出了修改，运行这个命令将触发Django的自动检测机制，以识别模型的任何更改，并随后自动生成相应的迁移脚本。这些生成的脚本会被储存在项目的`migrations/`目录下。通常情况下，你需要为每个应用程序运行这个命令，确保迁移脚本正确记录了模型的变化。
```python
python manage.py migrate
```
而这个命令则负责将生成的迁移脚本应用到数据库中。在你对模型文件进行更改后，首先运行`makemigrations`以生成迁移脚本，接着运行`migrate`来将这些脚本应用到数据库。对于新生成的迁移脚本，Django会按顺序逐个执行它们，从而更新数据库结构，以反映你的模型更改。对于已经执行过的脚本，Django会自动跳过，避免重复执行相同的操作。
## Django-models的常用字段和常用配置

**常用字段**

`CharField` 用于存储字符串类型，有最大长度限制

`IntegerField` 用于存储整数类型

`FloatField`用于存储浮点数类型

`BooleanField` 用于存储布尔类型

`DateField` 用于存储日期类型

`DateTimeField` 用于存储日期和时间类型

`ImageField` 用于存储图片类型

`FileField` 用于存储文件类型

`ForeignKey` **外键** 用于表示数据库表之间的关联关系

`OneToOneField` **一对一** 用于表示一对一的关联关系

`ManyToManyField` **多对多** 用于表示多对多的关联关系
　　‍
**常用配置**

`max_length` 字段的最大长度限制，可以应用于多种不同的字段类型。

`verbose_name` 字段的友好名称，便于在管理员后台可视化操作时使用。

`default` 指定字段的默认值。

`null` 指定字段是否可以为空。

`null=True` 设置允许该字段为 NULL 值

`blank` 指定在表单中输入时是否可以为空白。

`choices` 用于指定字段的可选值枚举列表,在最上面定义

## 字段定义
```python      
class Status(TextChoices):
    QUALIFIED = ('qualified', '良品')`
    UNQUALIFIED = ('unqualified', '不良品')`
status = CharField(max_length=32, choices=Status.choices, default=Status.QUALIFIED, verbose_name='状态')`
```

`TextChoices` 是 Django 3.0 引入的一个枚举类，用于在模型字段中创建可选择的、文本值的选项。
`related_name` 指定在多对多等关系中反向使用的名称。 
`on_delete` 指定如果外键关联的对象被删除时应该采取什么操作。

## Django-admin 引入admin后台和管理员
### 创建管理员
在终端运行命令
```python
python manage.py createsuperuser
```
执行命令后：
> (Django) G:\Django\Day2\myProject>python manage.py createsuperuser \
Username (leave blank to use 'lenovo'): day3 \
Email address: w2278257866@163.com \
Password:  \
Password (again): \
This password is too short. It must contain at least 8 characters. \ 
This password is too common. \
This password is entirely numeric. \
Bypass password validation and create user anyway? [y/N]: y \
Superuser created successfully.

登录 admin 后台
```python
python manage.py runserver
# http://127.0.0.1:8000/admin
```
### 配置
在**admin.py**文件中注册你的模型：

```python
from django.contrib import admin
from .models import * # 引入产品表

admin.site.register(Goods) # 注册产品表
admin.site.register(GoodsCategory) # 注册产品表
```

## 增加数据

```python
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


# Create your views here.
# GET
# POST

# 函数式编程
@api_view(['POST', 'GET'])
def InsertGoodsCategory(request):
    category_name = request.data.get('分类名字')

    # 获取分类对象或创建新的分类对象
    category, created = GoodsCategory.objects.get_or_create(name=category_name)

    # 判断是否已存在分类
    if not created:
        return Response({"status": "已存在", "goods_category": category_name}, status=200)
    else:
        return Response({"message": f"Successfully inserted category '{category_name}'."})


@api_view(['POST', 'GET'])
def FilterGoodsCategory(request):
    data = request.data.get('分类名字')
    goods = GoodsCategory.objects.filter(name=data)
    if goods.exists():
        return Response({"status": "已存在", "goods_category": data}, status=200)
    else:
        return Response({"status": "不存在", "goods_category": data}, status=404)
```

url.py
```python
from django.contrib import admin
from django.urls import path

from apps.myApp.views import FilterGoodsCategory, InsertGoodsCategory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('insertgoodscategory/', InsertGoodsCategory),
  ]
```
可以通过调用接口的方式增加新数据。