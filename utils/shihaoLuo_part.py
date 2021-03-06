import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from ian import InputData

class InputData_v2(InputData):
    '''
    This class is a good way to input all of the data. 
    It has a load_data() and find_rows() method that filter through the raw data.
    '''
    def __init__(self):
        InputData.__init__(self)
        
    def sum_data(self):
        return self.data.sum()
    

def main():
    print 'Running shihaoLuo_part.py...'
    fig, axs = plt.subplots(9,2, figsize=(15, 30))
    fig.subplots_adjust(hspace = 0.5, wspace=0.0)
    axs = axs.ravel()

    try:
        CA_data = InputData_v2()
        CA_data.load_data('data/road-traffic-injuries-2002-2010.csv', 
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
    except Exception as e:
        print 'Trouble plotting CA data: {0}'.format(e)

###New York###
    try: 
        NY_data = InputData_v2()
        NY_data.load_data('data/NYaccidents.csv', 
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

        
        fig.savefig('results/shihao-CA.png')
        fig1.savefig('results/shihao-NY.png')
    except Exception as e:
        print 'Trouble plotting NY data: {0}'.format(e)

if __name__ == '__main__':
    main()