#1 
class MyClass: # create a class
    x = 5 # class property

#2 
p1 = MyClass() # create an object from the class
print(p1.x) # print property 'x'
del p1 # delete the object

#3 
p1 = MyClass() # create 3 different objects
p2 = MyClass()
p3 = MyClass()

print(p1.x) # print their properties
print(p2.x)
print(p3.x)

#4 
class Person:
    pass # empty class