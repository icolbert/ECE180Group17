import pandas as pd
import glob
import os

class InputData:

	def __init__(self):
		self.read_columns = [
			'geoname', 'reportyear', 'mode', 'severity', 'injuries', 'totalpop','poprate', 'LL95CI_poprate', 'UL95CI_poprate', 'poprate_se', 'poprate_rse',
			'avmttotal', 'avmtrate', 'LL95CI_avmtrate', 'UL95CI_avmtrate', 'avmtrate_se','avmtrate_rse'
			]

	def load_data(self, fname, read_columns=None):

		assert isinstance(fname, str), "fname is not a string: %s" % fname
		assert  (fname in [i for i in glob.glob('data/*.csv')]), "fname is not in data/"

		data = pd.read_csv(fname)
		if read_columns:
			self.data = data.filter(items=read_columns, axis=1)
		else:
			self.data = data.filter(items=self.read_columns, axis=1)

if __name__ == '__main__':

	filter_items = [
		'geoname', 'reportyear', 
		'mode', 'severity', 'injuries', 'totalpop',
		'poprate', 'avmttotal'
		]

	xdata = InputData()
	xdata.load_data('data/road-traffic-injuries-2002-2010.csv', read_columns=filter_items)

	xdata.data.to_csv('sample.csv')

