#1 
def my_generator(): # create a generator
    yield 1 # give numbers one by one
    yield 2
    yield 3

for value in my_generator(): # use a loop
    print(value)

#2 
def large_sequence(n):
    for i in range(n):
        yield i # saves computer memory

gen = large_sequence(1000000) # create many numbers
print(next(gen)) # get the first number
print(next(gen)) # get the second number
print(next(gen))

#3 
total = sum(x * x for x in range(10)) # calculate without creating a list
print(total)

#4 
def simple_gen():
    yield "Emil"
    yield "Tobias"
    yield "Linus"

gen = simple_gen() # call the generator
print(next(gen)) # get the next name
print(next(gen))
print(next(gen))