import random

list = ""
for i in range(0, 8):
    for j in range(0,16):
        num = random.randrange(0, 8)
        list +=  str(num) + ","
    list += "\n"

print list