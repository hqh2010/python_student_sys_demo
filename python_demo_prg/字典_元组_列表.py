#!/usr/bin/python
# 演示python的基本数据结构
shoplist = ['apple', 'mango', 'carrot', 'banana']
print("I have ", len(shoplist), " items to purchase")
for item in shoplist:
    print(item)
print('\n I also have to buy rice')
shoplist.append('rice')
print('my shopping list is now:', shoplist)
shoplist.sort()
print("after sort shoplist is:", shoplist)
print(shoplist[1])
print(shoplist[0:2])
print("shoplist is:", shoplist[:])
print("shoplist的最后一个元素是:", shoplist[-1]) # -1表示最后一个元素
print('apple' in shoplist)

# python元组tuple 元组的元素不可更改
name1=('一点水','二点水','三点水','四点水','五点水', 123)
print("元组3的元素是：", name1[3])
x,y,z,k,j,l=name1
print(z)
# 字典
ab = {'key1':123, 'key2':'item2', 'key3':1.73}

# 列表推导式
lista = [i + 1 for i in range(10) if i % 2 == 0]
print(lista)
str_list = ['hello', 'world', 'python', 'list']
new_list = [s for s in str_list if len(s) > 3]
print(new_list)
print(str_list.index('world'))
for key, value in ab.items():
    print("key is ", key, "value is:", value)