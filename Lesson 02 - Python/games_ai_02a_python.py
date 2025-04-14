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
print(b)  # b changed type - discouraged to do so! - choose different name
print(type(b))
b = "KCG"
print(type(b))

######
# Types
# They are inferred by the interpreter, writing in the code is not necessary but a good practice, helps to read the code

number: int = 42
number = number + 8  # okay if you accept mutability
number = "string"  # allowed by the interpreter, IDEs and linters give you warnings

######
# Strings formatting

string1: str = "Tokyo"
string2: str = "Kyoto"
string3: str = string1 + string2
print(string3)
print(f"{string1} and {string2}")

######
# If condition

number2: int = 5
if number2 == 1:
    print("a is 1")
elif number2 == 2:
    print("a is 2")
else:
    print("a is something else")

if a == 1 or a == 2 or a == 3:
    print("a is 1 or 2 or 3")

number3 = 7
number4 = 3
if number3 == 7 and number4 == 3:
    print("a is 7 and b is 3")

number5 = 71
print("a is 71") if number5 == 71 else print("a is something else")

######
# For loop

words: list[str] = ["machine", "learning", "in", "python"]
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

i: int = 1
while i < 6:
    print(i)
    i += 2


######
# Functions


def test(param1: int | str, param2: int = 0) -> int:
    print(param1)
    print(param2)
    return param2 + 5


result1: int = test("aa")
print(result1)
print("--")
result2: int = test(14, 7)
print(result2)

######
# Imports

import os  # This will be at the beginning of the file in general code

print(os.listdir())
if not os.path.exists("test"):
    os.mkdir("test")
print(os.listdir())

os.rmdir("test")
print(os.listdir())

######
# Lists

x: list[int | str] = [1, 2, 31]
print(x)
print(x[1])
print(x[-1])

x.append(8)
print(x)
print(len(x))

x.append("hello")
print(x)

value: int | str = x.pop()
print(value)
print(x)

x.remove(31)
print(x)

x.reverse()
print(x)

######
# Dictionaries

japan: dict[str, str | int | list[str]] = {
    "name": "Japan",
    "short": "JP",
    "capital": "Tokyo",
    "population": 123_900_000,
    "neighbors": []
}
print(japan)
print(japan["name"])
print(japan.keys())

czechia: dict[str, str | int | list[str]] = {
    "name": "Czechia",
    "short": "CZ",
    "capital": "Prague",
    "population": 10_700_000,
    "neighbors": ["Germany", "Slovakia", "Poland", "Austria"]
}
print(czechia)

######
# Try-Catch-Finally

y: list[int] = [5, 7, 8]
try:
    y.remove(10)
except ValueError:
    print("Value of 10 is not in the list")
finally:
    y.clear()

print(y)
