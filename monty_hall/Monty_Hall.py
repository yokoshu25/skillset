import random


prise = ["car", "goat", "goat"]
doors = []

while (len(prise) > 0):
    prisenumber = random.randrange(len(prise))
    doors.append(prise.pop(prisenumber))
    print(doors)
    
choice = eval(input("Which door? (0 to 2): "))
choice1 = doors[choice]

print("Show the behind of door")

while(True):
    randDoor = random.randrange(len(doors))
    if doors[randDoor] != "car" and choice1 != randDoor:
        opened_door = doors[randDoor]
        break
print("Take a look at {}".format(opened_door))

print(doors)

switch = int(input("Do you want to switch? 0 = No 1 = Yes : "))
if switch == 0: 
    result = choice1
else:
    while(True):
        randDoor1 = random.randrange(len(doors))
        if doors[randDoor1] != opened_door and choice1 != randDoor1:
            break
    result = doors[randDoor1]
    

print(result)