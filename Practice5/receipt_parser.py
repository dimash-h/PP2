import re

#1
text = "abbb"
x = re.search("ab*", text)
print(x)
#2
text = "abb"
x = re.search("ab{2,3}", text)
print(x)
#3
text = "hello_world test_text example"
x = re.findall("[a-z]+_[a-z]+", text)
print(x)
#4
text = "Hello World Python"
x = re.findall("[A-Z][a-z]+", text)
print(x)
#5
text = "axxxb"
x = re.search("a.*b", text)
print(x)
#6
text = "Hello, world. Python"
x = re.sub("[ ,.]", ":", text)
print(x)
#7
text = "snake_case_string"
words = text.split("_")
print(words[0] + words[1].capitalize() + words[2].capitalize())
#8
text = "HelloWorldPython"
x = re.split("(?=[A-Z])", text)
print(x)
#9
text = "HelloWorldPython"
x = re.sub("(?=[A-Z])", " ", text)
print(x.strip())
#10
text = "camelCaseString"
x = re.sub("([A-Z])", "_\\1", text).lower()
print(x)