import pandas as pd

tacos = pd.read_csv('final_final_tacos.csv')
restaurants = pd.read_csv('restaurants.csv')
state_data = pd.read_csv('state_data.csv')

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
state = ''
if j_file.get('results'):
    location = j_file.get('results')[0].get('geometry').get('location')
    lat_long = (location.get('lat'), location.get('lng'))
    for object in j_file.get('results')[0].get('address_components'):
        if "administrative_area_level_1" in object.get('types'):
            state = object.get('short_name')
            break

from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 3958.8

lat1 = radians(lat_long[0])
lon1 = radians(lat_long[1])
in_radius_rows = []
for index, row in restaurants.iterrows():
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
count = 0
for row, distance in in_radius_rows:
    price_bin = ''
    if row['priceRangeCategory']:
        if(row['priceRangeCategory'] == 1):
            price_bin = '($)'
        if(row['priceRangeCategory'] == 2):
            price_bin = '($$)'
        if(row['priceRangeCategory'] == 3):
            price_bin = '($$$)'
    print(row['name'] + ' ' + price_bin, 'in', row['city'] + ', ' + row['state'], distance, 'miles away')
    if count < 5:
        for index, inner_row in tacos.iterrows():
            if row['id'] == inner_row['id']:
                out = '***** Menu Item: ' + inner_row['menus.name']
                if row['menus.amountMax'] != -1:
                    out += ' at $' + str(row['menus.amountMax'])
                print(out)
        count += 1
    else:
        print('*** Serves ' + "{0:.1f}%".format(float(row['taco_ratio']) * 100) + ' tacos and ' + "{0:.1f}%".format(row['burrito_ratio'] * 100) + ' burritos')
        print("* {0:.1f}%".format(float(row['meat_ratio']) * 100) + ' meat items')
        print("* {0:.1f}%".format(float(row['seafood_ratio']) * 100) + ' seafood items')
        print("* {0:.1f}%".format(float(row['vegetarian_ratio']) * 100) + ' vegetarian items')
        print("* {0:.1f}%".format(float(row['breakfast_ratio']) * 100) + ' breakfast items')
        print("* {0:.1f}%".format(float(row['other_ratio']) * 100) + ' misc. items')
    if row['restaurant_count'] > 1:
        print('******* This restaurant has ' + str(row['restaurant_count'] - 1) + ' other location(s) nationwide')
    else:
        print('******* This restaurant is the only location nationwide')
print('***********************')
print(state + ' data:')
row = ''
for index, roww in state_data.iterrows():
    if state == roww['state']:
        row = roww
print('*** Serves ' + "{0:.1f}%".format(float(row['taco_ratio']) * 100) + ' tacos and ' + "{0:.1f}%".format(row['burrito_ratio'] * 100) + ' burritos')
print("* {0:.1f}%".format(float(row['meat_ratio']) * 100) + ' meat items')
print("* {0:.1f}%".format(float(row['seafood_ratio']) * 100) + ' seafood items')
print("* {0:.1f}%".format(float(row['vegetarian_ratio']) * 100) + ' vegetarian items')
print("* {0:.1f}%".format(float(row['breakfast_ratio']) * 100) + ' breakfast items')
print("* {0:.1f}%".format(float(row['other_ratio']) * 100) + ' misc. items')

    #print stats
    #print # of locations
