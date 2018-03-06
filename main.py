import os

from utils import *

if __name__ == '__main__':
	filter_items = [
		'geoname', 'reportyear', 
		'mode', 'severity', 'injuries', 'totalpop',
		'poprate', 'avmttotal', 'county_name'
		]

	filter_dict = {
	'geoname': 'San Diego',
	'severity': 'Killed',
	'mode': None,
	'reportyear': range(2002,2011)
	}

	xdata = InputData()
	xdata.load_data('data/road-traffic-injuries-2002-2010.csv')

	# Bus, All modes, Bicyclist
	xs = {}
	for m in ['All modes', 'Bus', 'Bicyclist', 'Car/Pickup', 'Motorcycle', 'Truck', 'Pedestrian', 'Vehicles']:
		filter_dict['mode'] = m
		xs.update({m: xdata.filter_data(xdata.find_rows(filter_dict))})
		print('\n')

	for key, data in xs.items():
		a = BuildModel(data, ylabel=filter_dict['severity'])
		a.all(key)


	### Applying same code to Annual Miles Travelled

	filter_items = [
		'geoname', 'reportyear', 'region_code'
		'mode', 'ratio_type', 'ratio', 'county_name'
		]

	filter_dict = {
	'geoname': 'California',
	'mode': None,
	'reportyear': range(2002,2011)
	}
	miles_data = InputData()
	miles_data.load_data('data/annual-miles-traveled-2002-2010.csv')
	xs = {}
	for m in ['Bicyclist', 'Pedestrian', 'Vehicle']:
		filter_dict['mode'] = m
		xs.update({m: xdata.filter_data(xdata.find_rows(filter_dict))})
		print('\n')

	for key, data in xs.items():
		a = BuildModel(data, ylabel='Miles Traveled per Square Mile')
		#a.LinReg(key)
		#a.QuadReg(key)
		a.all(key)