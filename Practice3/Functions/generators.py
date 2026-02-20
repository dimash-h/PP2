#1
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)
#2
def large_sequence(n):
  for i in range(n):
    yield i

# This doesn't create a million numbers in memory
gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))
#3
# Calculate sum of squares without creating a list
total = sum(x * x for x in range(10))
print(total)
#4
def simple_gen():
  yield "Emil"
  yield "Tobias"
  yield "Linus"

gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))
