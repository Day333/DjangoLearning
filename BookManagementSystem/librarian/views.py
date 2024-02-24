from django.shortcuts import render
from librarian import models
from django.core.paginator import Paginator
from faker import Faker
from django.shortcuts import render, redirect, HttpResponse

# 注册视图函数
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        models.Librarian.objects.create(name=username, nickname=nickname, password=password)

        return redirect('/librarian/login/')

    return render(request, 'register.html')

# 登录
def login(request):
    error_msg = ''
    if request.method == 'POST':

        username = request.POST.get('username')
        pwd = request.POST.get('password')
        print("username---------------->", username)

        # 查询用户
        ret = models.Librarian.objects.filter(name=username, password=pwd)

        if ret:
            # 用户存在
            request.session['username'] = username
            librarian_obj = ret.last()  # 获取librarian对象
            nickname = librarian_obj.nickname
            request.session['nickname'] = nickname
            # 将用户的id 保存到session中
            request.session['id'] = librarian_obj.id
            return redirect('/librarian/book_list/')

        else:
            # 没有此用户-->> 用户名或者密码错误
            error_msg = '用户名或者密码错误请重新输入'
    return render(request, 'login.html', {'error_msg': error_msg})


# 登出
def logout(request):
    # 1. 将session中的用户名、昵称删除
    request.session.flush()
    # 2. 重定向到 登录界面
    return redirect('/librarian/login/')

# 装饰器
def librarian_decorator(func):
    def inner(request, *args, **kwargs):
        username = request.session.get('username')
        nickname = request.session.get('nickname')
        if username and nickname:
            """用户登录过"""
            return func(request, *args, **kwargs)
        else:
            """用户没有登录，重定向到登录页面"""
            return redirect('/librarian/login/')

    return inner


# 出版社操作
@librarian_decorator
def add_publisher(request):
    if request.method == 'POST':
        # 1.获取内容
        publisher_name = request.POST.get('publisher_name')
        publisher_address = request.POST.get('publisher_address')
        # 2.保存数据库
        models.Publisher.objects.create(name=publisher_name, address=publisher_address)
        # 3.重定向到类型列表
        return redirect('/librarian/publisher_list/')
    return render(request, 'publisher_add.html')


# 出版社列表
@librarian_decorator
def publisher_list(request, page=1):
    if request.method == "GET":
        publisher_obj_list = models.Publisher.objects.all()  # 获取出版社所有数据
        paginator = Paginator(publisher_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page if page else request.GET.get("page", 1)  # 当前页，默认显示第一页
        publisher_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 当前页
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)
        else:
            page_range = page_range
        return render(request, "publisher_list.html", locals())


@librarian_decorator
def update_publisher(request):
    """修改出版社"""
    if request.method == "GET":
        id = request.GET.get("id")
        publisher = models.Publisher.objects.get(id=id)
        return render(request, "publisher_update.html", locals())
    else:
        id = request.POST.get("id")
        names = request.POST.get("name")
        address = request.POST.get("address")
        models.Publisher.objects.filter(id=id).update(name=names, address=address)
        return redirect("/librarian/publisher_list/")


def delete_publisher(request):
    """删除出版社"""
    # 获取publisher_list.html页面传过来的id
    id = request.GET.get("id")
    #根据id，从数据库中获取出版社对象
    publisher = models.Publisher.objects.get(id=id)
    # 从数据库中删除该出版社对象
    publisher.delete()
    return redirect("/librarian/publisher_list/")

@librarian_decorator
def add_book(request):
    """添加图书"""
    if request.method == "GET":
        # 从数据库中查询所有出版社对象
        publisher_list = models.Publisher.objects.all()
        # 将页面转调到添加图书的页面
        return render(request, "book_add.html", locals())
    elif request.method == "POST":
        f = Faker(locale="zh_CN")  # 初始化Faker对象
        book_num = f.msisdn()  # 图书编码
        # 获取book_add.html表单提交过来的数据
        book_name = request.POST.get("book_name")
        author = request.POST.get("author")
        book_type = request.POST.get("book_type")
        book_price = request.POST.get("book_price")
        book_inventory = request.POST.get("book_inventory")
        book_score = request.POST.get("book_score")
        book_description = request.POST.get("book_description")
        book_sales = request.POST.get("book_sales")
        comment_nums = request.POST.get("comment_nums")
        publisher_id = request.POST.get("publisher")  # 出版社id
        publisher_obj = models.Publisher.objects.get(id=publisher_id)  # 出版社对象
        # 将表单获取到的数据保存到数据库中
        book_obj = models.Books.objects.create(
            book_num=book_num,
            book_name=book_name,
            author=author,
            book_type=book_type,
            book_price=book_price,
            book_inventory=book_inventory,
            book_score=book_score,
            book_description=book_description,
            book_sales=book_sales,
            comment_nums=comment_nums,
            publisher=publisher_obj,
        )
        # 保存图片
        # 注意上传字段使用 FILES.getlist() 来获取 多张图片
        userfiles = request.FILES.getlist('book_image')  # 图书缩略图
        # 循环遍历读取每一张图片保存到images下  -->>枚举 （0,'<InMemoryUploadedFile: 3.jpg (image/jpeg)>'）
        for index, image_obj in enumerate(userfiles):
            name = image_obj.name.rsplit('.', 1)[1]  # 图书格式
            path = 'librarian/static/images/books/{}_{}.{}'.format(book_name, index, name)  # 图片路径
            # 保存图片
            with open(path, mode='wb') as f:
                for content in image_obj.chunks():
                    f.write(content)

            # 2.保存图片路径到数据库
            obj_image = models.Image()
            path1 = 'images/books/{}_{}.{}'.format(book_name, index, name)
            obj_image.img_address = path1
            obj_image.img_label = image_obj.name  # 图片原名称
            obj_image.books = book_obj  # 设置图片和商品的关系
            obj_image.save()
            # 3.重定向到商品列表
        return redirect("/librarian/book_list")




def book_list(request, page=1):
    """图书列表"""
    if request.method == "GET":
        book_obj_list = models.Books.objects.all()
        paginator = Paginator(book_obj_list, 10)  # 实例化分页对象，每页显示10条数据
        total_page_num = paginator.num_pages  # 总页码
        current_page_num = page  # 当前页，默认显示第一页
        book_page_objs = paginator.page(current_page_num)  # 获取当页面的数据对象，用于响应前端请求进行渲染显示
        page_range = paginator.page_range  # 确定页面范围，以便进行模板渲染使用页码
        # 确定页码范围
        if total_page_num > 10:  # 当总页码大于10时
            if current_page_num < 9:  # 当前页小于10时
                page_range = range(1, 11)
            elif current_page_num + 8 > total_page_num:  # 当前页码是倒数第8页时
                page_range = range(current_page_num - 2, total_page_num + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 8)

        return render(request, "book_list.html", locals())



@librarian_decorator
def update_book(request):
    """修改图书"""
    if request.method == "GET":
        # 1.获取book_list.html页面传过来的id
        id = request.GET.get("id")
        # 2.从数据库中获取要修改的图书对象
        book_obj = models.Books.objects.get(id=id)
        # 3. 获取所有的出版社数据
        publisher_list = models.Publisher.objects.all()
        return render(request, "book_update.html", locals())

    else:
        # 获取book_update.html表单提交过来的数据
        id = request.POST.get("id")
        book_name = request.POST.get("book_name")
        book_type = request.POST.get("book_type")
        author = request.POST.get("author")
        book_price = request.POST.get("book_price")
        book_inventory = request.POST.get("book_inventory")
        book_score = request.POST.get("book_score")
        book_description = request.POST.get("book_description")
        book_sales = request.POST.get("book_sales")
        comment_nums = request.POST.get("comment_nums")
        publisher_id = request.POST.get("publisher")  # 出版社id
        publisher_obj = models.Publisher.objects.get(id=publisher_id)  # 出版社对象
        # 将表单提交过来的数据保存到数据库
        book_obj = models.Books.objects.filter(id=id).update(
            book_name=book_name,
            book_type=book_type,
            author=author,
            book_price=book_price,
            book_inventory=book_inventory,
            book_score=book_score,
            book_description=book_description,
            book_sales=book_sales,
            comment_nums=comment_nums,
            publisher=publisher_obj,
        )
        # 重定向到图书列表页面
        return redirect("/librarian/book_list")


def delete_book(request):
    """删除图书"""
    #  1. 获取book_list.html传来的id
    id = request.GET.get("id")
    # 2. 根据id，从数据库中获取出版社对象并且删除
    models.Books.objects.get(id=id).delete()
    # 3.  删除数据后返回到出版社列表页面。
    return redirect("librarian:book_list")
