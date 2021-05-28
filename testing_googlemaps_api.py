import googlemaps
import pandas as pd
import json
import geopy
import geopy.distance
import math
import numpy as np
import webbrowser
import time

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
    distance_interval = speed * interval
    return_path = []
    for index in range(len(directions) - 1):
        lat1 = directions[index][0]
        lng1 = directions[index][1]
        lat2 = directions[index + 1][0]
        lng2 = directions[index + 1][1]
        rads = np.arccos((lat1 * lat2 + lng1 * lng2) / ((lat1 ** 2 + lng1 ** 2) ** (1 / 2) *
                                                        (lat2 ** 2 + lng2 ** 2) ** (1 / 2)))
        angle = rads * (180/math.pi)
        distance_temp = distances[index]
        return_path.append((lat1, lng1))
        while distance_temp > distance_interval:
            distance_temp -= distance_interval

            origin = geopy.Point(lat1, lng1)
            destination = geopy.distance.GeodesicDistance(meters=distance_interval).destination(origin, angle)

            lat3 = destination.latitude
            lng3 = destination.longitude

            lat1 = lat3
            lng1 = lng3

            return_path.append((lat3, lng3))
    return return_path


            # query = "https://www.google.com/maps/search/?api=1&query={},{}".format(lat1, lng1)
            # webbrowser.open(query, new=0, autoraise=False)
            # time.sleep(2)

        #     print(f"{index} start: {str(directions[index]).rjust(40 + len(str(index)) + 8, ' ')}")
        #     print(f"{index} inter: {str((lat3, lng3)).rjust(40 + len(str(index)) + 8, ' ')}")
        # print(f"{index} end: {str(directions[index + 1]).rjust(40 + len(str(index)) + 10, ' ')}")

for x in get_complete_path(2, 12, directions, distances):
    print(x)

# For Śmietan:
# https://www.wolframalpha.com/input/?i=sqrt%28%28x+-+2%29%5E2+%2B+%28y+-+1%29%5E2%29+%3D+20
# https://www.google.com/search?q=distance+between+two+points&oq=distance+between+two+points+&aqs=chrome..69i57j0l9.11105j0j7&sourceid=chrome&ie=UTF-8
# https://sciencing.com/convert-distances-degrees-meters-7858322.html
