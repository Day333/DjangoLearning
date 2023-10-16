相关代码地址：[https://github.com/Day333/DjangoLearning](https://github.com/Day333/DjangoLearning)
# Day1
## 1 创建环境
首先，创建虚拟环境。
> conda create -n Django python=3.8

激活虚拟环境。
> conda activate Django

安装Django。
> pip install django

安装相关库：
安装DRF、Django-Filter、Django Spectacular、debug_toolbar、django_extensions 。
> pip install djangorestframework

> pip install django-filter

> pip install drf_spectacular

> pip install django-debug-toolbar

> pip install django_extensions

## 2 创建Django项目和APP
创建项目的命令：
> django-admin startproject myProject

注意，如果这里是在终端中创建，需要切换到对应的环境中。
此命令将会创建一个名为myProject的项目。
创建APP的命令（需要在外层的myProject文件中）：
> python manage.py startapp myApp

此时代码结构为：
> G:.                         
> └─myProject                 
>     │  manage.py            
>     │                       
>     ├─myApp                 
>     │  │  admin.py
>     │  │  apps.py
>     │  │  models.py
>     │  │  tests.py
>     │  │  views.py
>     │  │  __init__.py
>     │  │
>     │  └─migrations
>     │          __init__.py
>     │
>     └─myProject
>         │  asgi.py
>         │  settings.py
>         │  urls.py
>         │  wsgi.py
>         │  __init__.py
>         │
>         └─__pycache__
>                 settings.cpython-38.pyc
>                 __init__.cpython-38.pyc

## 3 启动项目
在myProject文件下的setting.py文件中在INSTALLED_APPS集合中加入：
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.erp_test', # 新加
    'rest_framework', # 新加
    'django_filters', # 新加
    'drf_spectacular' # 新加
]
```
运行项目先执行数据库相关操作，再启动 django 项目
**数据库迁移操作**
> python manage.py makemigrations

> python manage.py migrate

**启动Django服务**
> python manage.py runserver

运行此命令后，访问本地[http://127.0.0.1:8000](http://127.0.0.1:8000)即可看到界面。
