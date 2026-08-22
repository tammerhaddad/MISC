import os
import random

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meals.txt')
with open(path, 'r', encoding='utf-8') as file:
    meals = [line.strip() for line in file if line.strip()]
random_meals = random.sample(meals, min(10, len(meals)))
for i, meal in enumerate(random_meals, 1):
    print(f"{i}. {meal}")
