#During a break, Joan proposes a friendly show of their skills. 
#The 20 members of Joan's and Arthurs party are divided into two groups of 10 
#while the team has 3 members from Joans party and 3 members from Arthur party. 
#How many ways are there to choose the two teams? Explain your solution.


def createGroups(groups, groupSizes):
    currnum = 0
    returngroups = []
    for i in range(groups):
        tempreturngroup = []
        for j in range(groupSizes[i]):
            tempreturngroup + [currnum]
            currnum += 1
            print(f"{i} {j} {currnum}")
        returngroups + [tempreturngroup]
    return returngroups


print(createGroups(2, [2, 4]))