import random

starches = "rice, potatoes, pasta, bread".split(", ")
protein = "black beans, baked beans, chicken, beef, pork, fish, spam".split(", ")
flavor = "teriyaki, salty, bbq, indian spice, sour, chili, savory".split(", ")
food = [starches, protein, flavor]

for i in range(10):
    nums = [i[random.randrange[len(i)]] for i in food]
    print(f"{i+1}. {nums[0]}, {nums[1]}, {nums[2]}")