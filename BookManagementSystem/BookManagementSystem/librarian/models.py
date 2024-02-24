from django.db import models

# Create your models here.
# 管理员
class Librarian(models.Model):
    name = models.CharField(max_length=32, verbose_name="用户名")  # 用户名
    nickname = models.CharField(max_length=32, verbose_name="昵称")  # 昵称
    password = models.CharField(max_length=32, verbose_name="密码")  # 密码

# 出版社数据模型
class Publisher(models.Model):
    name = models.CharField(max_length=128, verbose_name="出版社名称")  # 出版社名称
    address = models.CharField(max_length=128, verbose_name="出版社地址")  # 出版社地址


# 图书数据模型
class Books(models.Model):
    book_num = models.CharField(max_length=32, verbose_name="图书编号")  # 图书编号
    book_name = models.CharField(max_length=128, verbose_name="图书名称")  # 图书名称
    author = models.CharField(max_length=255, verbose_name="作者") # 作者
    book_type = models.CharField(max_length=32, null=False,verbose_name="图书类型")  # 图书类型
    book_price = models.DecimalField(max_digits=5, decimal_places=2, default=10.01,verbose_name="图书价格")  # 图书价格
    book_inventory = models.IntegerField(verbose_name="图书库存")  # 图书库存
    book_score = models.DecimalField(max_digits=5, decimal_places=1, default=10.0,verbose_name="图书评分")  # 评分
    book_description = models.TextField(verbose_name="图书简介")  # 图书简介
    book_sales = models.IntegerField(verbose_name="图书销量")  # 图书销量
    comment_nums = models.IntegerField(default=0, verbose_name="评论量")  # 评论量
    publisher = models.ForeignKey(to='Publisher', on_delete=models.CASCADE, verbose_name="出版社名称")  # 出版社和图书一对多关系


# 图片数据
class Image(models.Model):
    img_address = models.ImageField(verbose_name="图片路径")  # 图片路径 -->> 会将路径封装成一个对象，需要使用模块Pillow,python 3.6 后 使用 PIL 模块
    img_label = models.CharField(max_length=128,verbose_name="图片名称")  # 图片名称
    books = models.ForeignKey(to='Books', on_delete=models.CASCADE,verbose_name="图书")  # 图书的图片


# 作者
class Author(models.Model):
    name = models.CharField(max_length=128,verbose_name="作者名称")
    books = models.ManyToManyField(to='Books',related_name="author_book",verbose_name="图书")

# 用户
class User(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")
    nickname = models.CharField(max_length=32,verbose_name="用户昵称")
    password = models.CharField(max_length=32,verbose_name="密码")
    phone = models.CharField(max_length=11,verbose_name="电话号码") # 电话
    last_time = models.DateTimeField(auto_now=True,verbose_name="登录时间")
    books = models.ManyToManyField(to="Books",verbose_name="图书")