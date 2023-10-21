# Day3

## QuerySet
QuerySet是从数据库中查询结果的集合。Django的ORM涉及三个主要类：Manager、QuerySet、和Model。每个Model默认都配备了一个名为`objects`的manager实例。这个`objects`属性提供了一个数据操作的API，并使用`Model.objects`方法返回符合查询条件的QuerySet。

```python
class QuerySet(model=None, query=None, using=None)[source]
```
QuerySet有以下两大特性：

1. **惰性**：只有在真正需要数据时，它才会去数据库中获取。例如，创建、过滤、切片和传递一个QuerySet并不会立即触发数据库操作，这就是所谓的惰性执行。
2. **缓存**：使用同一个QuerySet时，第一次查询会触发数据库操作，但Django会缓存结果。后续使用此QuerySet会从缓存中读取，从而减少了数据库查询。

**操作说明**
考虑以下数据表定义：

```python
class Goods(DjangoPeople):
    number = CharField(max_length=32, verbose_name='编号')
    name = CharField(max_length=64, verbose_name='名称')
    unit = CharField(max_length=64, verbose_name='单位')
    remark = CharField(max_length=256, verbose_name='备注')
```

主要操作及示例：

- `all()`: 查询所有对象

```python
DjangoPeople.objects.all()
```
- filter(**kwargs): 查询符合条件的数据
```python
DjangoPeople.objects.filter(name="abc")
DjangoPeople.objects.filter(name="x").filter(unit="y")
```
- get(): 查询单一对象，但可能返回多个值。
- delete(): 删除符合条件的对象
```python
categories_to_delete = DjangoPeople.objects.filter(name="abc")
deleted_count = categories_to_delete.delete()
```
- update(): 更新符合条件的对象的字段值。
- create(): 创建并保存新对象
```python
created_category = DjangoPeople.objects.create(name="abc")
```
- count(): 计算符合条件的对象数。
- order_by(): 对象排序，字段名前加“-”为降序。

**Instance功能**
Instance是Django模型的一个实例，对应数据库中的一条数据。与QuerySet（查询多个对象）相对，Instance针对单个对象进行创建、更新或删除。

基本操作示例：

- 创建
```python
Obj = Model(attr1=val1, attr2=val2)
Obj.save()
```
- 更新
```python
Obj = Model.objects.get(id=xxx)
Obj.attr1 = val1
Obj.save()
```
- 删除
```python
Obj = Model.objects.get(id=xxx)
Obj.delete()
```
总结：QuerySet用于多对象查询和聚合操作，而Instance主要用于单个对象的CRUD操作。