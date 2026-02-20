#1 
def my_function(): # create a function
    print("Hello from a function")

my_function() # call the function

#2 
def fahrenheit_to_celsius(fahrenheit): # create a function with a parameter
    return (fahrenheit - 32) * 5 / 9 # return the result

print(fahrenheit_to_celsius(77)) # you can call it many times
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#3 
def get_greeting():
    return "Hello from a function" # return text

message = get_greeting() # save result to a variable
print(message)

#4 
def my_function():
    pass # empty function