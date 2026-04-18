import os
import requests
from dotenv import dotenv_values, load_dotenv

#loading my API key from the config file
load_dotenv("config.env")
my_usda_api_key = os.getenv("usda_api_key")

#this is the base url from the usda webite, later in the function,
#I will add the necessary missing characters
base_usda_url = "https://api.nal.usda.gov/fdc/v1/foods/"

#Here I wanna ask the user to enter the food item
food_name_global = input("please input your food name: ")

#let's try to get info from the USDA website using our API key,
#I will do it using parameters inside the function below
def usda_food_info_receiver(food_name_local):
    usda_response = requests.get(f"{base_usda_url}search?api_key={my_usda_api_key}&query={food_name_local}%20")
    if usda_response.status_code != 200:
        print(f"sorry bad I can't pull data from the server the error is: {usda_response}")
    else:
        return usda_response.json()

print(usda_food_info_receiver(food_name_global))






