import googlemaps
import pandas as pd
import json
import numpy as np

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
    distance_metric_interval = speed * interval
    for index in range(len(distances)):
        distance_metric = distance_metric_interval
        distance = distances[index]
        centering_vector = (-directions[index][0], -directions[index][1])
        # x_a, y_a = directions[index]
        x_b, y_b = directions[index + 1]
        # a = (y_a - y_b) / (x_a - x_b)
        # b = -a * x_b + y_b
        while distance_metric < distance:
            x_a = 1
            y_a = 0
            x_b = x_b + centering_vector[0]
            y_b = y_b + centering_vector[1]
            rads = np.arccos((x_a * x_b + y_a * y_b) / ((x_a ** 2 + y_a ** 2) ** (1 / 2) *
                                                        (x_b ** 2 + y_b ** 2) ** (1 / 2)))
            if y_b < 0:
                rads = 2 * np.pi - rads

            x_c = np.sin(rads) * (distance_metric * (1 / 110540)) - centering_vector[0]
            y_c = np.cos(rads) * (distance_metric * (1 / 111320 * np.cos(x_c))) - centering_vector[1]

            # Latitude: 1 deg = 110540 m
            # Longitude: 1 deg = 111320 * cos(latitude) m

            print(f"{index} start: {str(directions[index]).rjust(40 + len(str(index)) + 8, ' ')}")
            print(f"{index} end: {str(directions[index + 1]).rjust(40 + len(str(index)) + 10, ' ')}")
            print(f"{index} inter: {str((x_c, y_c)).rjust(40 + len(str(index)) + 8, ' ')}")

            distance_metric += distance_metric


get_complete_path(2, 12, directions, distances)

# For Śmietan:
# https://www.wolframalpha.com/input/?i=sqrt%28%28x+-+2%29%5E2+%2B+%28y+-+1%29%5E2%29+%3D+20
# https://www.google.com/search?q=distance+between+two+points&oq=distance+between+two+points+&aqs=chrome..69i57j0l9.11105j0j7&sourceid=chrome&ie=UTF-8
# https://sciencing.com/convert-distances-degrees-meters-7858322.html
