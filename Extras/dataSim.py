"""Summary
    Script to create simulated data. Data is stored in simData3.txt
"""
import random


data = []

for j in range(50):
    curr = []
    m = random.randint(1, 3)
    b = random.randint(1, 2)

    for i in range(10):
        y = m * (i**.5) + b
        curr.append(y)
    data.append(curr)

for j in range(50):
    curr = []
    m = random.randint(1, 3)
    b = random.randint(1, 2)
    for i in range(10):

        y = m * (-i + 10)**.5 + b
        curr.append(y)
    data.append(curr)


with open('simData3.txt', 'w') as file:
    for feature in data:
        line = str(feature)
        file.write(line)
        file.write('\n')