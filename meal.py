import random
with open('meals.txt', 'r') as file:
    meals = file.readlines()
random_meals = random.sample(meals, 3)
for i, meal in enumerate(random_meals, 1):
    print(f"{i}. {meal.strip()}")
