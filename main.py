import os
import requests
from dotenv import dotenv_values, load_dotenv
from pprint import pprint
import pandas as pd

#loading my API key from the config file
load_dotenv("config.env")
my_usda_api_key = os.getenv("usda_api_key")

#this is the base url from the usda webite, later in the function,
#I will add the necessary missing characters
base_usda_url = "https://api.nal.usda.gov/fdc/v1/foods/"

#Here I wanna ask the user to enter the food item
# asking the user :food_name_global = input("please input your food name: ")
#for now we can use one variable for testing
food_name_global = input("Please enter a food item: ")

#let's try to get info from the USDA website using our API key,
#I will do it using parameters inside the function below
def usda_food_info_receiver(food_name_local):
    usda_response = requests.get(f"{base_usda_url}search?api_key={my_usda_api_key}&query={food_name_local}%20")
    if usda_response.status_code != 200:
        print(f"Sorry, I can't pull data from the server the error is: {usda_response}")
    else:
        return usda_response.json()

returned_info_usda = usda_food_info_receiver(food_name_global)

#the returned_info_usda is a massive dictionary, containing different levels,
#in each level we got lists of dictionaries inside each one we might find more useful info
#Here i will create another function that will extract the useful info for us
#The info that might be useful for the app is anything related to the nutrition values of the food
#that includes, energy, macronutrients, and micronutrients.. so this is what we will try to extract
#the dictionary in one example case had 7 main keys one of which is called "foods" that interest us
#inside the USDA database we have different datatypes such as Branded and Foundation
#for now we will extract the data related to the foundation only

def usda_food_info_extractor(usda_data):
    #first step is to get into the food level
    first_level = usda_data['foods']
    foundation_data = []

    #My decision is for now extract the data related to foundation:
    #I will just loop through the first_level variable just created
    #I will add each dictionary that is inside the foundation datatype

    for item in first_level:
        if item['dataType'] == 'Foundation':
            foundation_data.append(item)

    #ok let's try to show the user all the found matches, he will choose the number
    #and based on the chosen number we can drilldown into the data

    print(f"Good news, I have found {len(foundation_data)} matches")
    for i, j in enumerate(foundation_data):
        print(f"the item number {i}: {j['description']}")
    chosen_number = int(input("Please choose your desired item number: "))
    chosen_item = foundation_data[chosen_number]

    # the chosen food item here is now a dictionary, the key we need is called "foodNutrients"
    #let's drilldown to the key as well

    chosen_item_nutrients = chosen_item['foodNutrients']
    
    #ok at this point user has chosen the desired item, we can drill down
    #I will extract and show the calorie for finishing the day
    calorie_list = []
    for info in chosen_item_nutrients:
        if 'Energy' in info['nutrientName']:
            calorie_list.append(info)
    calorie_list2 = []
    for i in calorie_list:
        calorie_list2.append(i['value'])

    print(calorie_list2)

#let's try

if returned_info_usda is not None:
    print(f"""The API call for the food item {food_name_global}
       from USDA database has been successful. I will clean the data now""")
    extracted_info_usda = usda_food_info_extractor(returned_info_usda)
else:
    print(f"Sorry I was not able to get data from USDA for {food_name_global}")









