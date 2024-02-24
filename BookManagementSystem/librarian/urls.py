from django.urls import path, re_path
from librarian import views

app_name = "librarian"

urlpatterns = [
    path('register/', views.register),  # 注册功能
    path('login/', views.login),  # 登录功能
    path('logout/', views.logout),  # 登出功能

    #出版社模块
    path('add_publisher/', views.add_publisher),
    path("publisher_list/", views.publisher_list, name="publisher_list"),
    path("publisher_list/<int:page>", views.publisher_list, name="publisher_list"),
    path("update_publisher/", views.update_publisher, name="update_publisher"),
    path("delete_publisher/", views.delete_publisher, name="delete_publisher"),

    # 图书管理模块
    path("add_book/", views.add_book, name="add_book"),
    path("book_list/", views.book_list, name="book_list"),
    path("book_list/<int:page>", views.book_list, name="book_list"),
    path("update_book/", views.update_book, name="update_book"),
    path("delete_book/", views.delete_book, name="delete_book"),
]