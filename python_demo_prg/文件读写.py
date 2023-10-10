fp = open('D:/python_project/111.txt', 'w',encoding='utf-8')
print('奋斗成就更好的你', file=fp)
fp.close()

with open('D:/python_project/111.txt', 'a+',encoding='utf-8') as wfile:
    wfile.write('奋斗成就更好的你~~~')