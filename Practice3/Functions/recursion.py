#1 
def countdown(n): 
    if n <= 0:
        print("Done!")
    else:
        print(n)
        countdown(n - 1) # function calls itself

countdown(5) 

#2 
import sys
sys.setrecursionlimit(2000) # change the limit to avoid errors
print(sys.getrecursionlimit())

#3 
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2) # recursion

print(fibonacci(7))

#4 
def factorial(n): # calculate factorial
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1) # function calls itself

print(factorial(5))