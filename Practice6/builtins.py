from functools import reduce

nums = [1, 2, 3, 4]

# map
print("map:", list(map(lambda x: x*2, nums)))

# filter
print("filter:", list(filter(lambda x: x%2==0, nums)))

# reduce
print("reduce:", reduce(lambda a, b: a+b, nums))

# enumerate
for i, v in enumerate(nums):
    print("index:", i, "value:", v)

# zip
names = ["A", "B", "C", "D"]
for n, num in zip(names, nums):
    print(n, num)

# type conversion
x = "10"
print(type(x))
print(int(x))