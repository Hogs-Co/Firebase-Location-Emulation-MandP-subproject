from zipfile import ZipFile
from lxml import html
import os

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
			coords = []
			coords = coord.replace(' ', '').replace('\n', '').split(',')
			coords.remove('0')
			for index in range(len(coords)):
				coords[index] = float(coords[index])
			list_of_return_coords.append(coords)
	return list_of_return_coords


def give_start_points():
	return format_kml(start_doc)


def give_end_points():
	return format_kml(end_doc)

