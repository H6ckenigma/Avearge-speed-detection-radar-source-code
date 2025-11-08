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