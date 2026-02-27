#1
def square(n):
    for i in range(n + 1):
        yield i * i
#2
def even(n):
    for x in range(n + 1):
        if x % 2 == 0:
            yield x
#3
def divis(n):
    for x in range(0, n + 1):
        if x % 3 == 0 and x % 4 == 0:
            yield x
#4
def squares(a, b):
    for x in range(a, b + 1):
        yield x * x
#5
def countdown(n):
    for x in range(n, -1, -1):
        yield x

for x in countdown(5):
    print(x)