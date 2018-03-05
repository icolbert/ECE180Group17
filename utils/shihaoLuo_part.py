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
        #assert  (fname in [i for i in glob.glob('data/*.csv')]), "fname is not in data/"

        print 'Reading in {0}...'.format(fname) 
        self.data = pd.read_csv(fname)
        try:
            if read_columns:
                self.data = self.data.filter(items=read_columns, axis=1)
            else:
                self.data = self.data.filter(items=self.read_columns, axis=1)
        except Exception as e:
            print e

    def filter_data(self, x=None):
        if x.empty:
            N = self.data.sum()
            bad_columns = list(set(N[N == 0].index).union(set(set(list(self.data)) - set(N.index))))
            self.data = self.data.drop(bad_columns, axis=1)
        else:
            assert isinstance(x, type(pd.DataFrame())), "x needs to be a pandas DataFrame, it is a {0}".format(type(x))

            print 'Filtering bad features from data...'
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
            print 'Filtering {0}...'.format(key)
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
        
    def sum_data(self):
        return self.data.sum()
    

if __name__ == '__main__':
    fig, axs = plt.subplots(9,2, figsize=(15, 30))
    fig.subplots_adjust(hspace = 0.5, wspace=0.0)
    axs = axs.ravel()

    CA_data = InputData()
    CA_data.load_data('D:\Users\lsh\Desktop\ECE180/road-traffic-injuries-2002-2010.csv', 
                      ['reportyear', 'county_name','mode', 'severity', 'injuries'])
    year = map(str, range(2002, 2011))
    severity1 = ['Severe Injury', 'Killed']
    explode = [0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    for i in range(len(year)):
        for j in range(len(severity1)):
            filter_dict = {
            'mode': 'All modes',
            'severity': severity1[j],
            'reportyear': year[i], 
            }
            rows = CA_data.find_rows(filter_dict)
            new_rows = rows.groupby('county_name').sum()
            y = new_rows['injuries'].tolist()
            x_label = new_rows.index.values.tolist()
            y, x_label = zip(*sorted(zip(y, x_label), reverse=True))
            y = y[:9]
            x_label = x_label[:9]
            #axs[2*i+j].bar(x_label[1:-1], y[1:-1],align='center')
            axs[2*i+j].pie(y, startangle=180, autopct='%1.1f%%', pctdistance=0.5, labeldistance=1.2, explode=explode)
            axs[2*i+j].set_title(year[i] + ' ' + severity1[j])
            axs[2*i+j].axis('equal') 
            axs[2*i+j].legend(labels=x_label, loc = 'best')#, fontsize=10, bbox_to_anchor=(0.7, 0.87)) 
    
    fig1, axs1 = plt.subplots(1,2, figsize=(25, 5))
    fig1.subplots_adjust(hspace = 0.1, wspace=0.0)
    axs1 = axs1.ravel()

###New York###
    NY_data = InputData()
    NY_data.load_data('D:\Users\lsh\Desktop\ECE180/accidents.csv', 
                      ['BOROUGH', 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED', 
                       'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED', 
                       'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED'])
    #NY_sum = NY_data.sum_data()
    severity2 = ['INJURED', 'KILLED']
    #y1 = [33326, 78228, 37635, 59276, 9713]#injured
    #y2 = [132, 309, 183, 281, 57]#killed
    #y_hand = [y1, y2]
    for i in range(len(severity2)):
        rows = NY_data.data.groupby('BOROUGH').sum()
        #rows = NY_sum.filter(like=severity2[i], axis=0)
        new_rows = rows.filter(like=severity2[i], axis=1)
        x_label = rows.index.tolist()
        y = new_rows.sum(axis=1).tolist()
        y, x_label = zip(*sorted(zip(y, x_label), reverse=True))
        axs1[i].pie(y, startangle=180, autopct='%1.1f%%', pctdistance=0.5, labeldistance=1.2)
        axs1[i].set_title('NY '+severity2[i])
        axs1[i].axis('equal')
        axs1[i].legend(labels=x_label, fontsize=10, bbox_to_anchor=(0.7, 0.75)) 

    
    fig.savefig('./CA.png')
    fig1.savefig('./NY.png')
