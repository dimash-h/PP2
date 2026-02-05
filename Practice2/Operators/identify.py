#1
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)
#2
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)
#3
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)
print(x is y)