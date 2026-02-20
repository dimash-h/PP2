#1 
def myfunc():
    x = 300 # local variable, works only inside
    print(x)

myfunc()

#2 
x = 300 # global variable, works everywhere

def myfunc():
    x = 200 # inside variable
    print(x)

myfunc() # prints 200
print(x) # prints 300

#3 
x = 300

def myfunc():
    global x # get the global variable
    x = 200 # change it

myfunc()
print(x) # now it is 200

#4 
def myfunc():
    x = 300
    def myinnerfunc(): # function inside a function
        print(x) # it sees 'x'
    myinnerfunc()

myfunc()