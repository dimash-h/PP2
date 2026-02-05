#1
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")
#2
a = 200
b = 33
c = 500
if a > b or a > c:
  print("At least one of the conditions is True")
#3
a = 33
b = 200
if not a > b:
  print("a is NOT greater than b")
#4
score = 85

if score >= 0 and score <= 100:
  print("Valid score")
else:
  print("Invalid score")
#5
username = "Tobias"
password = "secret123"
is_verified = True

if username and password and is_verified:
  print("Login successful")
else:
  print("Login failed")
