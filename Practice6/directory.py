import os
import shutil

# create folders
os.makedirs("myfolder/subfolder", exist_ok=True)

# list files
print("Files:", os.listdir("."))

# find txt files
for f in os.listdir("."):
    if f.endswith(".txt"):
        print("TXT:", f)

# move file
shutil.move("test.txt", "myfolder/test.txt")

# copy file
shutil.copy("myfolder/test.txt", "test2.txt")

print("Done")