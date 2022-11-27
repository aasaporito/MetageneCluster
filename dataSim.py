import random

data =[]

#sqrt(x)
for j in range(50):
    curr=[]
    m = 2*random.random() + .2 
    b = random.randint(1,3)* random.random()+.1

    for i in range(10):
        y = m*(i**.5)+b
        curr.append(y)
    data.append(curr)


#sqrt(-x+10)
for j in range(50):
    curr=[]
    m = 2*random.random() + .2 
    b = random.randint(1,3) * random.random()+.1
    for i in range(10):
        
        y = m*(-i+10)**.5+b
        curr.append(y)
    data.append(curr)


with open('simData2.txt','w') as file:
    for feature in data:
        line = str(feature)
        file.write(line)
        file.write('\n')
file.close()