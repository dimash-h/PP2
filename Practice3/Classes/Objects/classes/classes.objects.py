#1
class MyClass:
  x = 5
#2
p1 = MyClass()
print(p1.x)
del p1
#3
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#4
class Person:
  pass