import os
import requests
from dotenv import dotenv_values, load_dotenv
from pprint import pprint
import pandas as pd
from datetime import datetime

#loading my API key from the config file
load_dotenv("config.env")
#For my own use I will use the following API key 
#my_usda_api_key = os.getenv("usda_api_key")

#for public testing a demo API key is available:
my_usda_api_key = "DEMO_KEY"

#this is the base url from the usda webite, later in the function,
#I will add the necessary missing characters
base_usda_url = "https://api.nal.usda.gov/fdc/v1/foods/"

#Here I wanna ask the user to enter the food item
# asking the user :food_name_global = input("please input your food name: ")
#for now we can use one variable for testing
def food_name_input():
    food_name_chosen = input("Please enter a food item: ")

    #let's try to get info from the USDA website using our API key,
    #I will do it using parameters inside the function below
    def usda_food_info_receiver(food_name_local):
        usda_response = requests.get(f"{base_usda_url}search?api_key={my_usda_api_key}&query={food_name_local}%20")
        if usda_response.status_code != 200:
            print(f"Sorry, I can't pull data from the server the error is: {usda_response}")
        else:
            return usda_response.json()
    returned_info_usda_json = usda_food_info_receiver(food_name_chosen)

    return returned_info_usda_json, food_name_chosen

#the returned_info_usda_json is a massive dictionary, containing different levels,
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
    branded_data = []
    #My decision is for now extract the data related to foundation:
    #I will just loop through the first_level variable just created
    #I will add each dictionary that is inside the foundation datatype

    for item1 in first_level:
        if item1['dataType'] == 'Foundation':
            foundation_data.append(item1)

    #Here I will add a loop to extract Branded foods from the database, it is necessary for many items like pizza!
    
    for item2 in first_level:
        if item2['dataType'] == 'Branded':
            branded_data.append(item2)

    if len(foundation_data)==0 and len(branded_data)==0 :
        print("Sorry I was not able to find any match for the food item :(, Do you want to try again with another item or exit?")
        users_response = input(". Please select (y or n):")
        if users_response.lower()[0] == "y":
            main_app()
        elif users_response.lower()[0] == "n":
            return 0
    #I will choose one datatype and work with it. For now I will choose the foundation data as my priority. 
    #I will use an else if with foundation data as the priority, because in cas the found data is branded I need t show an info that is different

    #ok let's try to show the user all the found matches, he will choose the number
    #and based on the chosen number we can drilldown into the data

    elif len(foundation_data) != 0:
        print(f"Good news, I have found {len(foundation_data)} matches \n")
        for i, j in enumerate(foundation_data):
            print(f"item number {i}: {j['description']}")
        chosen_number = int(input("\nPlease choose your desired item number: "))
        chosen_item = foundation_data[chosen_number]

        # the chosen food item here is now a dictionary, the key we need is called "foodNutrients"
        #let's drilldown to the key as well

        chosen_item_nutrients = chosen_item['foodNutrients']

    elif len(branded_data) != 0:
        print(f"Good news, I have found {len(branded_data)} matches \n")
        for i, j in enumerate(branded_data):
            print(f"""item number {i}: {j['description']}, Brand: {j['brandName'] if j.get('brandName') else 'Brand name not available'}, Market Country: {j['marketCountry']}, Ingredients: {j['ingredients']}""")
        chosen_number = int(input("\nPlease choose your desired item number: "))
        chosen_item = branded_data[chosen_number]

        # the chosen food item here is now a dictionary, the key we need is called "foodNutrients"
        #let's drilldown to the key as well

        chosen_item_nutrients = chosen_item['foodNutrients']
        
        #ok at this point user has chosen the desired item, we can drill down
        #I will extract and return the nutrition values
        #calory finder:
    for info in chosen_item_nutrients:
        if (info['unitName'] == 'KCAL') and (info['nutrientNumber'] == '208'):
            calorie = info['value']
        elif (info['unitName'] =='KCAL') and (info['nutrientNumber'] == '957'):    	
            calorie = info['value']
    #protein finder:
        elif (info['nutrientName'] == 'Protein') and (info['nutrientNumber'] == '203'):
            protein = info['value']
    #carb finder:
        elif ('Carbohydrate' in info['nutrientName'] ) and (info['nutrientNumber'] == '205'):
            carbs = info['value']
    #fat finder:
        elif ('fat' in info['nutrientName'] ) and (info['nutrientNumber'] == '204'):
            fat = info['value']


    return {'Calorie':calorie, 'Protein':protein, 'Carbs': carbs, 'Fat': fat}


def main_app():
    returned_data = food_name_input()
    returned_info_usda_json_global = returned_data[0]
    food_name_global = returned_data[1]
    item_1_nutrition_facts = usda_food_info_extractor(returned_info_usda_json_global)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return returned_info_usda_json_global, food_name_global, item_1_nutrition_facts, now

#let's try
new_list = main_app()
if new_list[2] == 0:
    print("Hopefully next time I'll do better! Thank you for using Sciplate, see you again soon, Ryan :)")
else:
    print(f"""\nin 100 grams of {new_list[1]}, There are:\n
    \t{new_list[2]['Calorie']} calories
    \t{new_list[2]['Protein']} grams of protein
    \t{new_list[2]['Carbs']} grams of carbohydrates
    \t{new_list[2]['Fat']} grams of fat\n
    \tyour registered time for this item is: {new_list[3]}\n
Thank you for using Sciplate, see you again soon, Ryan :)\n""")

