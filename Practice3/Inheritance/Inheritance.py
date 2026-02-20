#1 
class Person: # parent class
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self): # class method
        print(self.firstname, self.lastname)

x = Person("John", "Doe") # create an object
x.printname() # call the method

#2 
class Student(Person): # child class
    def __init__(self, fname, lname):
        Person.__init__(self, fname, lname) # call the parent's function

#3 
class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname) # super() gets everything from the parent

#4 
class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)
        self.graduationyear = 2019 # add a new property