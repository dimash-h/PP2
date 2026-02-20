#1 
def my_function(*kids): # *kids if we don't know the number of arguments
    print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus") # pass many arguments

#2 
def my_function(**kid): # **kid for a dictionary (key-value)
    print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes") # pass with keys

#3 
def my_function(a, b, c): 
    return a + b + c # return the sum

numbers = [1, 2, 3] # create a list
result = my_function(*numbers) # unpack the list with *
print(result)

#4 
def my_function(greeting, *names):
    for name in names: # loop through names
        print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")