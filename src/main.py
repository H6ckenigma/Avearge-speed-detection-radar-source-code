# Main : Error Handling and Perfecting
import time
import os
import sys

# Files are there ?
def files_check():
    print("Checking files...")
    time.sleep(1)
    
    reqs = ["radar_conf.py", "Data_simulator.py", "Processor.py"]
    missing = []
    for f in reqs:
        if not os.path.exists(f):
            missing.append(f)
            print(f"The file {f} is not there")
        else:
            print(f"{f} is there")
        time.sleep(0.3)
    if missing:
        print("Install all the files for the program to work")
        sys.exit()
    else:
        print("Files are there!")
        print("")
        time.sleep(1)
files_check()

# Config Normal ?
def conf_check():
    try:
        from radar_conf import Distance, Speed_limit, Num_cars
        print(f"Distance: {Distance}")
        time.sleep(0.5)
        print(f"Speed limit: {Speed_limit} km/h")
        time.sleep(0.5)
        print(f"Number of cars: {Num_cars}")
        time.sleep(0.5)
        print("")
    except:
        print("Problem in config File")
        sys.exit()
conf_check()

#Simulating plates
def sim():
    try:
        print("Starting the simulation...")
        time.sleep(1)
        from Data_simulator import data_gen, gen_plate
        from radar_conf import Num_cars
        data_gen()
        print(f"Generated {Num_cars} Cars Succesfully, You can check in data folder")
        time.sleep(1)
    except:
        print("Problem in the Data Simulator")
        sys.exit()
sim()
print("")

# Processing everything
def process():
    try:
        print("Starting the process...")
        time.sleep(1)
        from Processor import process as run_process
        run_process()
        print("Done Processing")
    except:
        print("There is a Problem in the processor")
        sys.exit()
process()

print("")
time.sleep(1)

import pandas
from radar_conf import Num_cars

read = pandas.read_csv("../data/results.csv")
speeders = read[read['status'] == "High Speed"]

if len(speeders) == 0:
    print("There is no speeders")
else:
    speeders = speeders.sort_values(by='excess', ascending=False)

    top3 = speeders.head(3)
    print("TOP 3 SPEEDERS ARE")
    print("-" * 10)
    for i, row in top3.iterrows():
        print(f"Plate : {row['plate']}")
        print(f"Speed: {row['speed']}")
        print(f"Excess: {row['excess']}")
        print(f"City {row['city']}")
        print("-" * 10)
        print("")