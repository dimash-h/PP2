#1 
def changecase(func): # create a decorator
    def myinner():
        return func().upper() # make text BIG
    return myinner

@changecase # use the decorator
def myfunction():
    return "Hello Sally" # return text

print(myfunction()) # call the function

#2 
def changecase(func):
    def myinner():
        return func().upper()
    return myinner

@changecase
def myfunction():
    return "Have a great day!"

print(myfunction.__name__) # show the inner function's name

#3 
def myfunction(): # normal function
    return "Have a great day!"

print(myfunction.__name__) # show the normal function's name

#4 
def changecase(func):
    def myinner(*args, **kwargs): # accept any arguments
        return func(*args, **kwargs).upper()
    return myinner

@changecase
def myfunction(nam):
    return "Hello " + nam

print(myfunction("John"))