import random
with open('C:/Users/tamme/OneDrive/Desktop/Files/Code/MISC/meals.txt', 'r', encoding='utf-8') as file:
    meals = file.readlines()
random_meals = random.sample(meals, 10)
for i, meal in enumerate(random_meals, 1):
    print(f"{i}. {meal.strip()}")