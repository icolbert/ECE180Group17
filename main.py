import os
import argparse
import scipy
import sklearn as sk

from utils import *

def bool_filter(x):
	if x.lower() in ['true', 't', 'yes', 'y']:
		return True
	elif x.lower() in ['false', 'f', 'no', 'n']:
		return False
	else:
		raise NameError('[Yes/No] or [True/False]')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-run_all',
		type=bool_filter,
		default=False,
		help='Boolean flag. Run all? [True/False]'
	)
	parser.add_argument('-verbose',
		type=bool_filter,
		default=False,
		help='Boolean flag. Print statements? [True/False]'
	)


	args = parser.parse_args()

	filter_items = [
		'geoname', 'reportyear', 
		'mode', 'severity', 'injuries', 'totalpop',
		'poprate', 'avmttotal', 'county_name'
		]

	filter_dict = {
	'geoname': 'California',
	'severity': 'Severe Injury',
	'mode': None,
	'reportyear': range(2002,2011)
	}

	xdata = InputData(verbose=args.verbose)
	xdata.load_data('data/road-traffic-injuries-2002-2010.csv')

	# Bus, All modes, Bicyclist
	xs = {}
	for m in ['All modes', 'Bus', 'Bicyclist', 'Car/Pickup', 'Motorcycle', 'Truck', 'Pedestrian', 'Vehicles']:
		filter_dict['mode'] = m
		xs.update({m: xdata.filter_data(xdata.find_rows(filter_dict))})
		if args.verbose: print('\n')

	traffic_models = {}
	for key, data in xs.items():
		print key
		a = BuildModel(data, ylabel=filter_dict['severity'])
		a.all(key)
		traffic_models.update({key:a})
		print('\n')


	### Applying same code to Annual Miles Travelled
	filter_items = [
		'geoname', 'reportyear', 'region_code', 'groupquarters',
		'mode', 'ratio_type', 'ratio', 'county_name'
		]

	filter_dict = {
	'geoname': 'California',
	'ratio_type': 'Miles Per Square Mile',
	'mode': None,
	'reportyear': range(2002,2011)
	}
	miles_data = InputData()
	miles_data.load_data('data/annual-miles-traveled-2002-2010.csv', read_columns=filter_items)
	ms = {}
	for m in ['Bicyclist', 'Pedestrian', 'Vehicle']:
		filter_dict['mode'] = m
		ms.update({m: miles_data.filter_data(miles_data.find_rows(filter_dict))})
		if args.verbose: print('\n')

	miles_models = {}
	for key, data in ms.items():
		print key
		data.to_csv('test.csv')
		a = BuildModel(data,ydim='ratio', ylabel='Miles Traveled per Square Mile')
		a.all(key)
		miles_models.update({key: a})
		print '\n'
	
	if args.verbose:
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Bicyclist'].y_lin, miles_models['Bicyclist'].y_lin)
		print '\nBikers\nLinReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Bicyclist'].y_quad, miles_models['Bicyclist'].y_quad)
		print 'QuadReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Bicyclist'].y_poly, miles_models['Bicyclist'].y_poly)
		print 'Poly-4 :: R-squard: {0:.2f}, P-Value: {1:.2f}\n'.format(r, p)

		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Pedestrian'].y_lin, miles_models['Pedestrian'].y_lin)
		print 'Pedestrians\nLinReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Pedestrian'].y_quad, miles_models['Pedestrian'].y_quad)
		print 'QuadReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Pedestrian'].y_poly, miles_models['Pedestrian'].y_poly)
		print 'Poly-4 :: R-squard: {0:.2f}, P-Value: {1:.2f}\n'.format(r, p)

		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Vehicles'].y_lin, miles_models['Vehicle'].y_lin)
		print 'Vehicles\nLinReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Vehicles'].y_quad, miles_models['Vehicle'].y_quad)
		print 'QuadReg :: R-squard: {0:.2f}, P-Value: {1:.2f}'.format(r, p)
		slope, inter, r, p, std = scipy.stats.mstats.linregress(traffic_models['Vehicles'].y_poly, miles_models['Vehicle'].y_poly)
		print 'Poly-4 :: R-squard: {0:.2f}, P-Value: {1:.2f}\n'.format(r, p)

	if args.run_all:
		shihaoLuo_part.main()
		Tianxiang_work.main()
		LogMode.main()
		qianfengGuo_part.main()