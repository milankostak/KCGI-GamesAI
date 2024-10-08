######
# Comments and basic printing

print("test")
# single line comment

######
# Variables

a = 7
b = "Japan"
print(a)
print(b)
b = 5
print(b)  # b changed type
print(type(b))
b = "KCG"
print(type(b))

######
# Strings formatting

a = "Tokyo"
b = "Kyoto"
c = a + b
print(c)
print(f"{a} and {b}")

######
# If condition

a = 5
if a == 1:
    print("a is 1")
elif a == 2:
    print("a is 2")
else:
    print("a is something else")

if a == 1 or a == 2 or a == 3:
    print("a is 1 or 2 or 3")

a = 7
b = 3
if a == 7 and b == 3:
    print("a is 7 and b is 3")

a = 71
print("a is 71") if a == 71 else print("a is something else")

######
# For loop

words = ["machine", "learning", "in", "python"]
for word in words:
    print(word)
print("--")

for number in range(2, 10):
    print(number)
print("--")

for number in range(2, 15, 3):
    print(number)

######
# While loop

i = 1
while i < 6:
    print(i)
    i += 2

######
# Functions


def test(param1, param2=0):
    print(param1)
    print(param2)
    return param2 + 5


result1 = test("aa")
print(result1)
print("--")
result2 = test(14, 7)
print(result2)

######
# Imports

import os  # In general code, this will be at the beginning of the file

print(os.listdir())
if not os.path.exists("test"):
    os.mkdir("test")
print(os.listdir())

os.rmdir("test")
print(os.listdir())

######
# Lists

x = [1, 2, 31]
print(x)
print(x[1])
print(x[-1])

x.append(8)
print(x)
print(len(x))

x.append("hello")
print(x)

value = x.pop()
print(value)
print(x)

x.remove(31)
print(x)

x.reverse()
print(x)

######
# Dictionaries

japan = {
    "name": "Japan",
    "short": "JP",
    "capital": "Tokyo",
    "population": 123_900_000,
    "neighbors": []
}
print(japan)
print(japan["name"])
print(japan.keys())

czechia = {
    "name": "Czechia",
    "short": "CZ",
    "capital": "Prague",
    "population": 10_700_000,
    "neighbors": ["Germany", "Slovakia", "Poland", "Austria"]
}
print(czechia)

######
# Try-Catch-Finally

y = [5, 7, 8]
try:
    y.remove(10)
except ValueError:
    print("Value of 10 is not in the list")
finally:
    y.clear()

print(y)
