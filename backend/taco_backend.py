import pandas as pd

tacos = pd.read_csv('final_final_tacos.csv')

address = input("Please enter the central street address: ").split()
city = input("Please enter the city: ")
state = input("Please enter the state (2 letter format): ")
postal = str(input("Please enter the postal code: "))
desired_radius = float(input("Desired search radius in miles? "))

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

from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 3958.8

lat1 = radians(lat_long[0])
lon1 = radians(lat_long[1])
in_radius_rows = []
for index, row in tacos.iterrows():
    lat2 = radians(row['latitude'])
    lon2 = radians(row['longitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance < 0:
        print("OH NO!!!!!")

    if distance < desired_radius:
        in_radius_rows.append((row, distance))

in_radius_rows.sort(key=lambda tup: tup[1])
for row, distance in in_radius_rows:
    print(row['menus.name'], 'at', row['name'], 'in', row['city'] + ', ' + row['state'], distance, 'miles away')
