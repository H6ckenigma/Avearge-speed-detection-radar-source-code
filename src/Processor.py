# Speed Calculation and Overall logic
import pandas
from radar_conf import Distance, Speed_limit
def process():
    a = pandas.read_csv("../data/radar_a.csv")
    b = pandas.read_csv("../data/radar_b.csv")
    
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

    merged['speed'] = speed.round(0).astype(int).astype(str) + "Km/h"
    merged['excess'] = merged['speed'].str.replace("Km/h", "").astype(int) - Speed_limit
    merged['excess'] = merged['excess'].clip(lower=0)
    #checker
    status = []
    for s in speed:
        if s > Speed_limit:
            status.append("High Speed")
        else:
            status.append("Good")
    
    merged['status'] = status

    merged.to_csv("../Data/results.csv", index=False)          

    bad = merged[merged['status'] == "High Speed"]
    if len(bad) > 0:
        print("The cars that has exceeded the limit are")
        print(bad[['plate', 'speed', 'excess', 'status']])
    else:
        print("All drivers are Good")
process()