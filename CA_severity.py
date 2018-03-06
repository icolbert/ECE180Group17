import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import re
from matplotlib import pyplot

def CA_severity(fname):
    #Read the data of California from the .csv file
    #input file = "road-traffic-injuries-2002-2010.csv"
    year = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
    severity = ['Killed', 'Severe Injury']
    mode = ['All modes', 'Bicyclist', 'Bus', 'Car/Pickup', 'Motorcycle', 'Pedestrian', 'Truck', 'Vehicles']
    interval = ['2002-2004','2005-2007','2008-2010']
    types = [mode[1], mode[5], mode[7]]

    bins = len(year)
    year_pos = []
    new_year_pos = []
    for y in year:
        y = int(y)
        year_pos.append(y)
        new_year_pos.append(y+0.25)
    #In this part, compare different types of accidents' injury line chart through year 2002 to 2010...
    #The variables num_K and num_S are the collected value of killed and severe injury, in this part they
    #have length of 9 zeros for all kinds of modes of accicent.
    for m in mode:
        #with open('C:/Winter 2018/ECE180/road-traffic-injuries-2002-2010.csv') as infile:
        with open(fname) as infile:
            reader = csv.reader(infile)
            num_K = [0 for _ in range(len(year))]
            num_S = [0 for _ in range(len(year))]    
            for idx,row in enumerate(reader):
                if row != '':
                    if row[5] == 'CA' and row[7] == 'California' and row[12] == m:                        
                        if row[13] == severity[0] and row[2] in year:
                            num_K[year.index(row[2])] += int(row[14])
                        elif row[13] == severity[1] and row[2] in year:
                            num_S[year.index(row[2])] += int(row[14])
                else:
                    break
            #This part is the line chart shows the trend of different travel types involved in severity.
            plt.plot(year, num_K, 'bs', year, num_S, 'g^', year, num_K, 'k', year, num_S, 'k')
            plt.title('California traffic injury severity data from year 2002 to 2010 of %s' %m)
            plt.xlabel('year')
            plt.ylabel('Severity')
            plt.gca().legend(('Killed','Severely Injury'))
            plt.show()
            #This part is the histogram of same type of travel mode .
            plt.bar(year_pos, num_K, 0.25, color = 'black')
            plt.bar(new_year_pos, num_S, 0.25, color = 'orange')
            plt.title('California traffic injury severity data from year 2002 to 2010 of %s' %m)
            plt.xlabel('year')
            plt.ylabel('Severity')
            plt.xticks(new_year_pos, year)
            plt.gca().legend(('Killed','Severely Injury'))
            plt.show()
        
    infile.close()
    ind = np.arange(len(interval))
    for t in types:
        #with open('C:/Winter 2018/ECE180/road-traffic-injuries-2002-2010.csv') as infile:
        with open(fname) as infile:
            reader = csv.reader(infile)
            AVMT_K = [0 for _ in range(len(interval))]
            AVMT_S = [0 for _ in range(len(interval))]
            for idx,row in enumerate(reader):
                if row != '':
                    if row[5] == 'CA' and row[7] == 'California' and row[12] == t:                        
                        if row[13] == severity[0] and row[2] in interval:
                            AVMT_K[interval.index(row[2])] += float(row[24])
                        elif row[13] == severity[1] and row[2] in interval:
                            AVMT_S[interval.index(row[2])] += float(row[24])
                else:
                    break
            #This part is the histogram of same type of travel mode, which plots AVMT rate according to
            #three interval from year 2002 to 2010. It shows the severity vs.usage of roads by each type of trasportation.
            plt.bar(ind, AVMT_K, 0.25, color = 'red', zorder = 2)
            plt.bar(ind+0.25, AVMT_S, 0.25, color = 'purple', zorder = 2)
            plt.xticks(ind, interval)
            plt.title('California traffic injury severity AVMT rate of %s' %t)
            plt.xlabel('year')
            plt.ylabel('AVMT rate')
            plt.gca().legend(('Killed','Severely Injury'))
            plt.show()
        
    infile.close()
    return
    