import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import re
from matplotlib import pyplot
from numpy import sum

def NY_severity(fname):
    #Read the data of NewYork from the .csv file
    #input file = "accidents.csv"
    year = ['2013', '2014', '2015', '2016', '2017', '2018']
    col_num = [6,8,10,12]
    mode = ['Persons', 'Cyclist', 'Motorist', 'Pedestrians']
    #Amount of killed/injured:
    person_killed = []
    person_injured = []
    cyclist_killed = []
    cyclist_injured = []
    motorist_killed = []
    motorist_injured = []
    pedestrian_killed = []
    pedestrian_injured = []
    #Ratio of killed/injured:
    ped_k = []
    ped_i = []
    cycl_k = []
    cycl_i = []
    motor_k = []
    motor_i = []

    for y in year:
        Total_num_K = [0 for _ in range(len(mode))]
        Total_num_S = [0 for _ in range(len(mode))]
        print y
        with open(fname) as infile:
    #     with open('accidents.csv') as infile:
            reader = csv.reader(infile)
            for idx,row in enumerate(reader):
                if idx == 0:
                    continue
                elif row != '':
                    if str(row[0][6:10]) == y:
                        num_k = [0 for _ in range(len(mode))]
                        num_s = [0 for _ in range(len(mode))]  
                        for col in col_num:
                            num_k[(col-6)/2] += int(row[col+1])
                            num_s[(col-6)/2] += int(row[col])
                        Total_num_K = map(lambda x,y: x+y,Total_num_K,num_k)
                        Total_num_S = map(lambda x,y: x+y,Total_num_S,num_s)   
                else:
                    break

        person_killed.append(Total_num_K[0])
        person_injured.append(Total_num_S[0])
        cyclist_killed.append(Total_num_K[2])
        cyclist_injured.append(Total_num_S[2])
        motorist_killed.append(Total_num_K[3])
        motorist_injured.append(Total_num_S[3])
        pedestrian_killed.append(Total_num_K[1])
        pedestrian_injured.append(Total_num_S[1])
        ped_k.append(Total_num_K[1]/float(Total_num_K[0]))
        ped_i.append(Total_num_S[1]/float(Total_num_S[0]))
        cycl_k.append(Total_num_K[2]/float(Total_num_K[0]))
        cycl_i.append(Total_num_S[2]/float(Total_num_S[0]))
        motor_k.append(Total_num_K[3]/float(Total_num_K[0]))
        motor_i.append(Total_num_S[3]/float(Total_num_S[0]))
    infile.close()

    #This is the line chart of each type of killed/injury in traffic report
    plt.plot(year, person_killed, 'bs', year, person_injured, 'g^', year, person_killed, 'k', year, person_injured , 'k')
    plt.title('NewYork traffic injury severity data from year 2013 to 2018 of %s' %mode[0])
    plt.xlabel('year')
    plt.ylabel('Severity')
    plt.gca().legend(('Killed','Injury'))
    plt.show()

    plt.plot(year, cyclist_killed, 'bs', year, cyclist_injured, 'g^', year, cyclist_killed, 'k', year, cyclist_injured , 'k')
    plt.title('NewYork traffic injury severity data from year 2013 to 2018 of %s' %mode[2])
    plt.xlabel('year')
    plt.ylabel('Severity')
    plt.gca().legend(('Killed','Injury'))
    plt.show()

    plt.plot(year, motorist_killed, 'bs', year, motorist_injured, 'g^', year, motorist_killed, 'k', year, motorist_injured , 'k')
    plt.title('NewYork traffic injury severity data from year 2013 to 2018 of %s' %mode[3])
    plt.xlabel('year')
    plt.ylabel('Severity')
    plt.gca().legend(('Killed','Injury'))
    plt.show()

    plt.plot(year, pedestrian_killed, 'bs', year, pedestrian_injured, 'g^', year, pedestrian_killed, 'k', year, pedestrian_injured , 'k')
    plt.title('NewYork traffic injury severity data from year 2013 to 2018 of %s' %mode[1])
    plt.xlabel('year')
    plt.ylabel('Severity')
    plt.gca().legend(('Killed','Injury'))
    plt.show()

    #This is bar chart that shows the percentage of each type
    ind =  np.arange(len(year))
    ratio_k = [ped_k, cycl_k, motor_k]
    ratio_i = [ped_i, cycl_i, motor_i]
    ratio_types = [ratio_k, ratio_i]

    for ratio in ratio_types:
        if ratio == ratio_types[0]:
            plt.bar(ind,ratio[0], 0.25, color = 'red', zorder = 2)
            plt.bar(ind+0.25, ratio[1], 0.25, color = 'purple', zorder = 2)
            plt.bar(ind+0.5, ratio[2], 0.25, color = 'grey', zorder = 2)
            plt.xticks(ind, year)
            plt.title('NewYork traffic accident severity weight ratio of killed')
            plt.xlabel('year')
            plt.ylabel('Weighted ratio')        
            plt.gca().legend(('Pedestrian','Cyclists','Motorist'))
            plt.show()
        else:
            plt.bar(ind,ratio[0], 0.25, color = 'red', zorder = 2)
            plt.bar(ind+0.25, ratio[1], 0.25, color = 'purple', zorder = 2)
            plt.bar(ind+0.5, ratio[2], 0.25, color = 'grey', zorder = 2)
            plt.xticks(ind, year)
            plt.title('NewYork traffic accident severity weight ratio of injured')
            plt.xlabel('year')
            plt.ylabel('Weighted ratio')        
            plt.gca().legend(('Pedestrian','Cyclists','Motorist'))
            plt.show()
    return