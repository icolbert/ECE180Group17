import os

from utils import ian

if __name__ == '__main__':
	xdata = ian.InputData()
	xdata.load_data('data/road-traffic-injuries-2002-2010.csv')

	xdata.data.to_csv('sample.csv')