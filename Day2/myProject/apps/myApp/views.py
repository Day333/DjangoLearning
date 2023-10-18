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