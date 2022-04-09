Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
product = ['Apple','Banana','Mango']
print(len(product))
3
product.append('Orage')
product
['Apple', 'Banana', 'Mango', 'Orage']
product.append('Coconut')
product
['Apple', 'Banana', 'Mango', 'Orage', 'Coconut']
product.remove('Coconut')
product
['Apple', 'Banana', 'Mango', 'Orage']
print(product[0])
Apple
print(product[1])
Banana
print(product[-1])
Orage
del product[-1]
product
['Apple', 'Banana', 'Mango']
product[2] = 'Orage'
product
['Apple', 'Banana', 'Orage']
product.insert(1,'Mango')
product
['Apple', 'Mango', 'Banana', 'Orage']
for pd in product:
    print(pd)

    
Apple
Mango
Banana
Orage
for i in range(10):
    print(i)

    
0
1
2
3
4
5
6
7
8
9
for i in range(1,11)
SyntaxError: expected ':'
for i in range(1,11):
    print(i)

    
1
2
3
4
5
6
7
8
9
10
list(range(10))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in [20,45,80]:
    print(i)

    
20
45
80
position = (500,1000)
print(position[0])
500
print(position[1])
1000
x,y = (500,700)
print(x)
500
print(y)
700
product = {'Mango':'Hery','Durain':'James','Apple':'Noy'}
print(product['Mango'])
Hery
print(product['Durain'])
James
print(product['Apple'])
Noy
product = {'Mango':['Hery','Robert'],'Durain':'James','Apple':'Noy'}
print(product['Mango'])
['Hery', 'Robert']
print(product['Mango'][1])
Robert
product = {'Mango':['Hery','Robert'],'Durain':'James','Apple':{'55205648':'Noy','25468721':'Bell'}}
print(product['Mango']['55205648'])
Traceback (most recent call last):
  File "<pyshell#45>", line 1, in <module>
    print(product['Mango']['55205648'])
TypeError: list indices must be integers or slices, not str
print(product['Apple']['55205648'])
Noy
