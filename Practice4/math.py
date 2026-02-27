import math
#1
deg = float(input())
print(f"{math.radians(deg):.6f}")
#2
h = float(input())
b1 = float(input())
b2 = float(input())
print((b1 + b2) * h / 2)
#3
n = int(input())
s = float(input())
print((n * (s ** 2)) / (4 * math.tan(math.pi / n)))
#4
base = float(input())
height = float(input())
print(base * height)