import pandas as pd
import glob
import os

class InputData:
	'''
	This class is a good way to input all of the data. 
	It has a load_data() and find_rows() method that filter through the raw data.
	'''
	def __init__(self):
		self.read_columns = [
			'geoname', 'reportyear', 'mode', 'severity', 'injuries', 'totalpop','poprate', 'LL95CI_poprate', 'UL95CI_poprate', 'poprate_se', 'poprate_rse',
			'avmttotal', 'avmtrate', 'LL95CI_avmtrate', 'UL95CI_avmtrate', 'avmtrate_se','avmtrate_rse'
			]

	def load_data(self, fname, read_columns=None):
		'''
		fname (type: str) - the filename needs the path and should be in 'data/'
		read_columns (type: list) - you can specify which columns you would like to read
		'''
		assert isinstance(fname, str), "fname is not a string: {0}".format(type(fname))
		assert  (fname in [i for i in glob.glob('data/*.csv')]), "fname is not in data/"

		self.data = pd.read_csv(fname)
		try:
			if read_columns:
				self.data = self.data.filter(items=read_columns, axis=1)
			else:
				self.data = self.data.filter(items=self.read_columns, axis=1)
		except Exception as e:
			print e

		N = self.data.sum()
		bad_columns = list(set(N[N == 0].index).union(set(data) - set(N.index)))
		self.data = self.data.drop(bad_columns, axis=1)

	def find_rows(self, filter_dict={'geoname':'California'}):
		'''
		filter_dict (type: dict) - feed a dictionary to filter the rows where the key is the columns
		and the value can either be a string or a list of values

		returns a filtered pandas DataFrame
		'''
		assert isinstance(filter_dict, dict), "filter_dict is not a dictionary: {0}".format(type(filter_dict))
		
		x = self.data
		for key, value in filter_dict.items():
			if isinstance(value, list):
				y = pd.DataFrame(data=[])
				for v in value:
					try:
						y = pd.concat([x[x[key] == str(v)], y], ignore_index=True)
					except Exception as e:
						print e
				x = y
			else:
				try:
					x = x[x[key] == value]
				except Exception as e:
					print e

		return x

if __name__ == '__main__':

	'''
	Last update: 2/12/2018 -ic 

	Testing the functions and classes in this file
	'''

	filter_items = [
		'geoname', 'reportyear', 
		'mode', 'severity', 'injuries', 'totalpop',
		'poprate', 'avmttotal'
		]

	filter_dict = {
	'geoname': 'California',
	'mode': 'Bus',
	'severity': 'Killed',
	'reportyear': range(2002,2011)
	}

	xdata = InputData()
	xdata.load_data('data/road-traffic-injuries-2002-2010.csv')
	xs = xdata.find_rows(filter_dict)

	xs.to_csv('sample.csv')


