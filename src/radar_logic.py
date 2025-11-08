# Speed Calculation and Overall logic
import pandas
from radar_conf import Distance, Speed_limit
def process():
    a = pandas.read.csv("../Data/radar_a.csv")
    b = pandas.read.csv("../Dara/radar_b.csv")
    
    #Datetime format
    a['time'] = pandas.to_datetime(a['time'])
    b['time'] = pandas.to_datetime(b['time'])
    
    merged = pandas.merge(a, b, on='plate')
    
    #delta t
    time_a = merged['time_x']
    time_b = merged['time_y']
    diff = time_b - time_a
    
    #Speed Calc
    h = diff.dt.total_seconds() / 3600
    speed = Distance / h

    merged['speed'] = speed
    
    #checker
    status = []
    for s in speed:
        if s > Speed_limit:
            status.append("High Speed")
        else:
            status.append("Good")
    
    merged['status'] = status

    merged.to_csv("../Data/results.csv", index=False)          

