import googlemaps
import pandas as pd
import json

gmaps = googlemaps.Client(key='AIzaSyCHMbZoZ4oY26FIVFU2xllmaWr70YRt004')

# Geocoding an address
geocode_result1 = gmaps.geocode('Łódź, Rydla 7a, Polska')
geocode_result2 = gmaps.geocode('Łódź, Wojewódzkiego 5, Polska')

result1 = geocode_result1[0]['geometry']['location']
result2 = geocode_result2[0]['geometry']['location']

location1 = (result1['lat'], result1['lng'])
location2 = (result2['lat'], result2['lng'])


def get_path(start_point, end_point):
    directions = gmaps.directions(start_point, end_point, 'walking')
    directions = json.dumps(directions)
    directions = pd.read_json(directions)

    directions = directions['legs'].to_json()
    directions = json.loads(directions)
    directions = pd.DataFrame(directions['0'])
    distance = dict(directions['distance'])[0]['value']

    directions = directions['steps'].to_json()
    directions = json.loads(directions)
    directions = pd.DataFrame(directions['0'])

    return_directions = [start_point]
    for index, row in directions.iterrows():
        return_directions.append(tuple([row['end_location']['lat'], row['end_location']['lng']]))

    return_distances = []
    for index, row in directions.iterrows():
        return_distances.append(row['distance']['value'])

    return distance, return_directions, return_distances


distance, directions, distances = get_path(location1, location2)
print(location1)
print(f"{distance}\n{directions}\n{distances}")


def get_complete_path(speed, interval, directions, distances):
    distance_metric = speed * interval
    for index in range(len(distances)):
        distance = distances[index]
        while (distance - distance_metric) > 0:
            distance -= distance_metric


get_complete_path(2, 10, directions, distances)

# For Śmietan:
# https://www.wolframalpha.com/input/?i=sqrt%28%28x+-+2%29%5E2+%2B+%28y+-+1%29%5E2%29+%3D+20
# https://www.google.com/search?q=distance+between+two+points&oq=distance+between+two+points+&aqs=chrome..69i57j0l9.11105j0j7&sourceid=chrome&ie=UTF-8
# https://sciencing.com/convert-distances-degrees-meters-7858322.html
