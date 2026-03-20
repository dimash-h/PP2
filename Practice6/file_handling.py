import shutil
import os

#create and write
f = open("test.txt", "w")
f.write("Hello\n")
f.write("World\n")
f.close()

#read 
f = open("test.txt", "r")
print("File content:")
print(f.read())
f.close()

#append
f = open("test.txt", "a")
f.write("New line\n")
f.close()

#check again
f = open("test.txt", "r")
print("After append:")
print(f.read())
f.close()

#copy file
shutil.copy("test.txt", "copy.txt")
print("File copied")

#delete safely
if os.path.exists("copy.txt"):
    os.remove("copy.txt")
    print("File deleted")