import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from ian import InputData
    

def main():
    print('Running LogMode.py...')
    fig, axs = plt.subplots(9,2, figsize=(15, 30))
    fig.subplots_adjust(hspace = 0.5, wspace=0.0)
    axs = axs.ravel()

    CA_data = InputData()
    CA_data.load_data('data/road-traffic-injuries-2002-2010.csv', 
                      ['reportyear', 'geoname', 'mode', 'severity', 'injuries'])
    year = map(str, range(2002, 2011))
    severity1 = ['Severe Injury', 'Killed']
    explode = [0.0, 0.0, 0.0, 0.1, 0.7, 1.3]
    for i in range(len(year)):
        for j in range(len(severity1)):
            filter_dict = {
            'geoname': 'California',
            'severity': severity1[j],
            'reportyear': year[i], 
            }
            rows = CA_data.find_rows(filter_dict)
            y = rows['injuries'].tolist()[1:-1]
            x_label = rows['mode'].tolist()[1:-1]
            y, x_label = zip(*sorted(zip(y, x_label), reverse=True))
            # axs[2*i+j].bar(x_label[1:-1], y[1:-1],align='center')
            axs[2*i+j].pie(y, startangle=180, autopct='%1.1f%%', pctdistance=0.5, labeldistance=1.2, explode=explode)
            axs[2*i+j].set_title(year[i] + ' ' + severity1[j])
            axs[2*i+j].axis('equal') 
            axs[2*i+j].legend(labels=x_label, loc = 'best')#, fontsize=10, bbox_to_anchor=(0.7, 0.87)) 
    
    fig1, axs1 = plt.subplots(1,2, figsize=(25, 5))
    fig1.subplots_adjust(hspace = 0.1, wspace=0.0)
    axs1 = axs1.ravel()

    NY_data = InputData()
    NY_data.load_data('data/accidents.csv', 
                      ['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED', 
                       'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED', 
                       'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED'])
    NY_sum = NY_data.data.sum()
    severity2 = ['INJURED', 'KILLED']
    for i in range(len(severity2)):
        rows = NY_sum.filter(like=severity2[i], axis=0)
        x_label = rows.index.tolist()
        y = rows.tolist()
        y, x_label = zip(*sorted(zip(y, x_label), reverse=True))
        axs1[i].pie(y, startangle=180, autopct='%1.1f%%', pctdistance=0.5, labeldistance=1.2)
        axs1[i].set_title('NY '+severity2[i])
        axs1[i].axis('equal')
        axs1[i].legend(labels=x_label, fontsize=10, bbox_to_anchor=(0.7, 0.75)) 

    fig.savefig('results/mode/CA.png')
    fig1.savefig('results/mode/NY.png')

if __name__ == '__main__':
    main()