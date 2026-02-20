#1 
def my_function(fname): # create a function with parameter 'fname'
    print(fname + " Refsnes")

my_function("Emil") # call the function
my_function("Tobias") 
my_function("Linus")

#2 
def my_function(name): # 'name' is a parameter
    print("Hello", name)

my_function("Emil") # 'Emil' is an argument

#3 
def my_function(fname, lname): # function with two parameters
    print(fname + " " + lname)

my_function("Emil", "Refsnes") # pass two arguments

#4 
def my_function():
    return ["apple", "banana", "cherry"] # return a list

fruits = my_function() # get the list from the function
print(fruits[0]) # print the first item
print(fruits[1])
print(fruits[2])