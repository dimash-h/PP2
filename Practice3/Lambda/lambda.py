#1 
x = lambda a : a + 10 # short function, adds 10
print(x(5)) # call it

#2 
def myfunc(n): 
    return lambda a : a * n # return a short function

mydoubler = myfunc(2) # now this function multiplies by 2
print(mydoubler(11))

#3 
numbers = [1, 2, 3, 4, 5] # create a list
doubled = list(map(lambda x: x * 2, numbers)) # multiply all by 2
print(doubled)

#4 
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x)) # sort by word length
print(sorted_words)