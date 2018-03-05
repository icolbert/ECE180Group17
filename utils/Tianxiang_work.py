from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
		#assert  (fname in [i for i in glob.glob('data\*.csv')]), "fname is not in data/"

		print('Reading in {0}...'.format(fname))
		self.data = pd.read_csv(fname)
		try:
			if read_columns:
				self.data = self.data.filter(items=read_columns, axis=1)
			else:
				self.data = self.data.filter(items=self.read_columns, axis=1)
		except Exception as e:
			print(e)

	def filter_data(self, x=None):
		if x.empty:
			N = self.data.sum()
			bad_columns = list(set(N[N == 0].index).union(set(set(list(self.data)) - set(N.index))))
			self.data = self.data.drop(bad_columns, axis=1)
		else:
			assert isinstance(x, type(pd.DataFrame())), "x needs to be a pandas DataFrame, it is a {0}".format(type(x))

			print('Filtering bad features from data...')
			N = x.sum()
			bad_columns = list(set(N[N == 0].index).union(set(set(list(x)) - set(N.index))))
			x = x.drop(bad_columns, axis=1)

			return x

	def find_rows(self, filter_dict={'geoname':'California'}):
		'''
		filter_dict (type: dict) - feed a dictionary to filter the rows where the key is the columns
		and the value can either be a string or a list of values

		returns a filtered pandas DataFrame
		'''
		assert isinstance(filter_dict, dict), "filter_dict is not a dictionary: {0}".format(type(filter_dict))
		
		x = self.data
		for key, value in filter_dict.items():
			print('Filtering {0}...'.format(key))
			if isinstance(value, list):
				y = pd.DataFrame(data=[])
				for v in value:
					try:
						y = pd.concat([x[x[key] == str(v)], y], ignore_index=True)
					except Exception as e:
						print(e)
				x = y
			else:
				try:
					x = x[x[key] == value]
				except Exception as e:
					print(e)

		return x

    
    
    
if __name__ == '__main__':
    
    CA_data = InputData()
    CA_data.load_data('../data/road-traffic-injuries-2002-2010.csv',
                      ['reportyear', 'severity','injuries'])
    

    severity = ['Severe Injury', 'Killed']
    plt.figure(figsize=(12,10))
    for i in  range(len(severity)):
        filter_dict = {
        'severity': severity[i]
        }
        
        rows = CA_data.find_rows(filter_dict)
        new_rows = rows.groupby('reportyear').sum()
        new_rows = new_rows.drop(['2002-2004','2005-2007','2006-2010','2008-2010'])
        new_rows.index = new_rows.index.astype(int)
            
        new = new_rows.groupby(new_rows.index).sum()
        
        y = new['injuries'].tolist()[0:len(new)]
        x_label = new.index.values.tolist()[0:len(new)]
        
        plt.bar(x_label,y,0.5,0.5)
        plt.xlabel('Year',fontsize=14)
        plt.ylabel('Number of victims',fontsize=14)        
        plt.title('Number of Injury and Killed vs. Years in CA',fontsize=18,fontweight="bold")
        plt.legend(labels = severity, loc = 'best')
    
    plt.savefig('./CA.png')
    plt.close()

################################## NY  
    #severity2 = ['Injured', 'Killed']
    NY_data = InputData()
    NY_data.load_data('../data/accidents.csv',[ 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 
                       'DATE'])
            
    da = NY_data.data

    da18 = da.groupby(da['DATE'].str.contains("2018", False)).sum()
    da17 = da.groupby(da['DATE'].str.contains("2017", False)).sum()
    da16 = da.groupby(da['DATE'].str.contains("2016", False)).sum()
    da15 = da.groupby(da['DATE'].str.contains("2015", False)).sum()
    da14 = da.groupby(da['DATE'].str.contains("2014", False)).sum()
    da13 = da.groupby(da['DATE'].str.contains("2013", False)).sum()
    da12 = da.groupby(da['DATE'].str.contains("2012", False)).sum()
    
    #fig1, axs1 = plt.subplots(figsize=(15, 15)) #1,2, 
    y= []
    y1 = []
    year = ['2018', '2017', '2016', '2015', '2014', '2013', '2012']
    severity2 = ['Number of Person Injured', 'Number of Person Killed']
    data_index = [da18,da17,da16,da15,da14,da13,da12]
    
    plt.figure(figsize=(12,10))
    #data_index[0].iloc[1,i]
    for i in  range(2): 
        for j in range(7):
            y.append(data_index[j].iloc[1,i])

        #plt.figure(figsize=(10,10))
        #gra1 = axs1.bar(year,y)
        
        plt.bar(year,y,0.5,0.5)
        #for a,b in zip(year, y):
        #    plt.text(a+1, b, str(b))

        plt.xlabel('Year',fontsize=14)
        plt.ylabel('Number of victims',fontsize=14)
        plt.title('Number of Injury and Killed vs. Years in NYC',fontsize=18,fontweight="bold")
        plt.legend(labels = severity2, loc = 2)
        y.clear()
    #gra1.savefig('./NY4.png')
    plt.savefig('./NY1.png')
    plt.close()
    
    plt.figure(figsize=(12,10))
    #fig2, axs2 = plt.subplots(figsize=(15, 15))
    for j in range(7):
            y1.append(data_index[j].iloc[1,1])
    #gra2 = axs1.bar(year,y1)
    plt.bar(year,y1,0.5,0.5)
    plt.xlabel('Year',fontsize=14)
    plt.ylabel('Number of victims',fontsize=14)    
    plt.title('Number of Killed vs. Years in NYC',fontsize=18,fontweight="bold")
    plt.legend(labels = severity2, loc = 1)
 
    plt.savefig('./NY2.png')
    #gra2.savefig('./NY5.png')
    plt.close()
