from zipfile import ZipFile
from lxml import html
import os
from random import randint
import googlemaps
import pandas as pd
import json
import geopy
import geopy.distance
import math
import numpy as np

gmaps = googlemaps.Client(key='AIzaSyCHMbZoZ4oY26FIVFU2xllmaWr70YRt004')

start_kmz = ZipFile(os.path.join('coords', 'start_points.kmz'), 'r')
end_kmz = ZipFile(os.path.join('coords', 'end_points.kmz'), 'r')

start_kml = start_kmz.open('doc.kml', 'r').read()
end_kml = end_kmz.open('doc.kml', 'r').read()

start_doc = html.fromstring(start_kml)
end_doc = html.fromstring(end_kml)


def format_kml(given_doc):
	list_of_return_coords = []
	for pm in given_doc.cssselect('Placemark'):
		tmp = pm.cssselect('track')
		if len(tmp):
			# Track Placemark
			tmp = tmp[0]  # always one element by definition
		# for desc in tmp.iterdescendants():
		# 	print("Skipping empty tag %s" % desc.tag)
		else:
			# Reference point Placemark
			coord = pm.cssselect('Point coordinates')[0].text_content()
			coords = coord.replace(' ', '').replace('\n', '').split(',')
			coords.remove('0')
			for index in range(len(coords)):
				coords[index] = float(coords[index])
			coords[::] = coords[::-1]
			list_of_return_coords.append(coords)
	return list_of_return_coords


def give_start_points():
	return format_kml(start_doc)


def give_end_points():
	return format_kml(end_doc)


def get_path(start_point, end_point):
	directions = gmaps.directions(start_point, end_point, 'walking')
	directions = json.dumps(directions)
	directions = pd.read_json(directions)

	directions = directions['legs'].to_json()
	directions = json.loads(directions)
	directions = pd.DataFrame(directions['0'])

	directions = directions['steps'].to_json()
	directions = json.loads(directions)
	directions = pd.DataFrame(directions['0'])

	return_directions = [start_point]
	for index, row in directions.iterrows():
		return_directions.append(tuple([row['end_location']['lat'], row['end_location']['lng']]))

	return_distances = []
	for index, row in directions.iterrows():
		return_distances.append(row['distance']['value'])

	return return_directions, return_distances


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


def get_random_path():
	start_points = give_start_points()
	end_points = give_end_points()

	start = start_points[randint(0, len(start_points) - 1)]
	end = end_points[randint(0, len(end_points) - 1)]

	directions, distances = get_path(start, end)

	return get_complete_path(2, 10, directions, distances)
