import requests

#this is the base url from the usda webite, later in the function,
#I will add the necessary missing characters
base_usda_url = "https://api.nal.usda.gov/fdc/v1/foods/"

#Here I wanna ask the user to enter the food item
food_name_global = input("please input your food name")

#let's try to get info from the USDA website using our API key,
#I will do it using parameters inside the function below
def usda_food_info_receiver(food_name_local):
    usda_response = requests.get(f"{base_usda_url}search?api_key=DEMO_KEY&query={food_name_local}%20")
    return usda_response

print(usda_food_info_receiver(food_name_global))






