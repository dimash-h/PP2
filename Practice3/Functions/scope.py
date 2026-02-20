#1
def myfunc():
  x = 300
  print(x)

myfunc()
#2
x = 300

def myfunc():
  x = 200
  print(x)

myfunc()

print(x)
#3
x = 300

def myfunc():
  global x
  x = 200

myfunc()

print(x)
#4
def myfunc():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc()