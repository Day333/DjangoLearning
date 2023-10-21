# Day4
## apiview
APIView 的概念

APIview 是 Django REST Framework 提供的一个视图类。它和 Django 中的 view 类有些相似，但是又有一些不同之处。APIview 可以处理基于 HTTP 协议的请求，并返回基于内容协商的响应，它旨在提供一个易于使用且灵活的方式来构建 API 视图。

```python
# 面向对象编程
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
#### APIView
 class GetGoods(APIView):
     def get(self, request):
         data = Goods.objects.all()
         serializer = GoodsSerializer(instance=data, many=True)
         print(serializer.data)
         return Response(serializer.data)

     def post(self, request):
         # 从请求数据中提取字段
         request_data = {
             "category": request.data.get("Goodscategory"),
             "number": request.data.get("number"),
             "name": request.data.get("name"),
             "barcode": request.data.get("barcode"),
             "spec": request.data.get("spec"),
             "shelf_life_days": request.data.get("shelf_life_days"),
             "purchase_price": request.data.get("purchase_price"),
             "retail_price": request.data.get("retail_price"),
             "remark": request.data.get("remark"),
         }

         # 使用 create() 方法创建新的商品对象
         new_goods = Goods.objects.create(**request_data)

         # 对创建的对象进行序列化，并作为响应返回
         serializer = GoodsSerializer(instance=new_goods)
         return Response(serializer.data)


 # 面向对象编程
 class FilterGoodsCategoryAPI(APIView):
     # request 表示当前的请求对象
     # self 表示当前实例对象

     def get(self, request, format=None):
         print(request.method)
         return Response('ok')

     def post(self, request, format=None):
         print(request.method)
         return Response('ok')

     def put(self, request, format=None):
         print(request.method)
         return Response('ok')
```

首先，self 表示当前实例对象，这里指的是视图类的实例对象。

request 表示当前的请求对象，包含了客户端发送的信息，例如请求头、请求体等。

pk 是 path 参数 int:pk，用于获取请求中的产品 ID。

format 表示客户端请求的响应格式，例如 JSON、XML 等。这个参数通常不需要指定，会根据客户端发送的 Accept 请求头来自动选择响应格式。如果客户端指定了响应格式，那么我们可以从请求中获取到这个参数并且做出相应的处理。

在这个方法中，我们需要通过 pk 参数获取到对应的产品数据，并将其序列化成 JSON 格式并返回给客户端。具体的实现方式可以参考序列化器文档和 Django ORM 文档。

## Serialization 序列化的高级使用

### 序列化器 `serializers`

#### 序列化器的作用

- 序列化将 `queryset` 和 `instance` 转换为 `json/xml/yaml` 返回给前端
- 反序列化与序列化则相反

#### 定义序列化器

- 定义类，继承自 `Serializer`
- 通常新建一个 `serializers.py` 文件 撰写序列化内容
- 使用 `suah as` 目前只支持
- `read_only` 只读
- `label` 字段说明信息
- `max_length` 最大长度

##### serializer.py

```python
# 定义产品序列化器
from rest_framework.serializers import *
from .models import *

# 产品分类序列化器
class GoodsCategorySerializer(ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('name', 'remark')

# 产品序列化器
class GoodsSerializer(ModelSerializer):
    # 外键字段相关的数据 需要单独序列化
    category = GoodsCategorySerializer()

    class Meta:
        model = Goods

        # 序列化单个字段
        fields = ('name',)

        # 序列化多个字段
        fields = ('name', 'number',)

        # 序列化所有字段
        fields = '__all__'
```

views.py

```python
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializer import *

class GetGoods(APIView):
    def get(self, request):
        data = Goods.objects.all()
        serializer = GoodsSerializer(instance=data, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        # 从请求数据中提取字段
        request_data = {
            "category": request.data.get("Goodscategory"),
            "number": request.data.get("number"),
            "name": request.data.get("name"),
            "barcode": request.data.get("barcode"),
            "spec": request.data.get("spec"),
            "shelf_life_days": request.data.get("shelf_life_days"),
            "purchase_price": request.data.get("purchase_price"),
            "retail_price": request.data.get("retail_price"),
            "remark": request.data.get("remark"),
        }

        # 使用 create() 方法创建新的商品对象
        new_goods = Goods.objects.create(**request_data)

        # 对创建的对象进行序列化，并作为响应返回
        serializer = GoodsSerializer(instance=new_goods)
        return Response(serializer.data)

```
urls.py
```python
from django.contrib import admin
from django.urls import path
from apps.erp_test.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filtergoodscategory/', FilterGoodsCategory),
    path('filtergoodscategoryapi/', FilterGoodsCategoryAPI.as_view()),
    path('getgoods/', GetGoods.as_view()),
]

```

## Django-DRF（ModelViewSet）

### 什么是DRF？

DRF，即Django REST framework，是Django提供的一个强大的Web API框架，用于构建灵活的Web APIs。在DRF中，ModelViewSet是一个视图集类，它封装了常见的模型操作方法。

ModelViewSet继承自以下类：

- GenericViewSet：提供一组通用的视图方法，方便实现特定功能。
- ListModelMixin：GET请求，用于获取资源列表。
- RetrieveModelMixin：GET请求，用于获取单个资源的详细信息。
- CreateModelMixin：POST请求，用于创建资源。
- UpdateModelMixin：PUT请求，用于更新资源。
- DestroyModelMixin：DELETE请求，用于删除资源。

### 如何使用

要使用ModelViewSet，需要设置`queryset`属性为要查询的对象集合，并设置`serializer_class`属性为对应的序列化器类。

#### 示例

**view.py**

```python
from rest_framework.viewsets import ModelViewSet

class YourModelViewSet(ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```
使用ModelViewSet后，你将自动获得默认的CRUD方法。
```python
from rest_framework.decorators import action

class GoodsCategoryViewSet(ModelViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_obj = GoodsCategory.objects.latest('id')
        print(latest_obj)
        return Response("Hello, you've called a custom function.")

```

serializer.py

```python
class GoodsSerializer(ModelSerializer):
    category = GoodsCategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'

```

这些技术知识点可以帮助我们快速构建出具有CRUD功能的Web应用，并且遵循了Django框架的惯例和最佳实践。通过使用这些技术知识点，我们能够提高开发效率，减少重复的代码编写工作，并且保证代码的一致性和可维护性。