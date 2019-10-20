import pandas as pd

tacos = pd.read_csv('final_final_tacos.csv')

address = input("Please enter the central street address: ").split()
city = input("Please enter the city: ")
state = input("Please enter the state (2 letter format): ")
postal = str(input("Please enter the postal code: "))

import requests
import json

api_call = "https://maps.googleapis.com/maps/api/geocode/json?address="
for elem in address:
    api_call += elem + '+'
api_call = api_call[:-1]
api_call += ',+' + city + ',+' + state + ',+'
if(len(str(postal)) == 4):
    api_call += '0'
api_call += postal + '&key=AIzaSyAAUh-OwNCVg-vY4_YZheCLGbLN5QZqJME'

j = requests.get(api_call)
j_file = j.json()
if j_file.get('results'):
    location = j_file.get('results')[0].get('geometry').get('location')
    lat_long = (location.get('lat'), location.get('lng'))
print(lat_long)
