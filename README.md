# Road Traffic Incident Analysis
## ECE 180 - Group 17
Using Python 2.7

#### Packages Used:
* Pandas
* Numpy
* Sklearn
* Scipy
* Os
* Matplotlib

How to use:

```shell
python main.py -run_all true -verbose false
```

__run_all__ :Boolean: run all of the plots used in the graph

__verbose__ :Boolean: print more throughout the model fitting

#### Goal
The project aims to analyze and predict the occurrence of severe road traffic injuries in various state. Our full California dataset is pulled from government Health Data at www.healthdata.gov,  where “injury data is from the Statewide Integrated Traffic Records System (SWITRS), California Highway Patrol (CHP), 2002-2010 data from the Transportation Injury Mapping System (TIMS)” [1]. We aim to get a more accurate model by factoring in Annual Miles Traveled, which is also provided by www.healthdata.gov [2]. Our New York data set is pulled from NYC OpenData [3].

#### Data
Severe injuries and deaths resulting from various modes of transportation in California and New York. Our data is pulled from https://www.healthdata.gov and https://data.cityonewyork.us.

#### Resources
[1] Road Traffic Injuries, 2002-2010. https://www.healthdata.gov/dataset/road-traffic-injuries

[2] Annual Miles Traveled, 2002-2010. https://www.healthdata.gov/dataset/annual-miles-traveled-2002-2010

[3] NYC Open Data: accidents. https://data.cityofnewyork.us/Public-Safety/accidents/yjf6-ewhz/data
