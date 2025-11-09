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

#Update
print("Starting Simulator", end="", flush=True)
time.sleep(0.5)
for i in range(3):
    print(".", end="", flush=True)
    time.sleep(0.5)
print("Ctrl+C to quit")
time.sleep(1)

from radar_conf import Distance, Speed_limit, radar_a_file, radar_b_file, results_file
from Data_simulator import gen_one_car, add_to_csv, gen_plate
from Processor import process
import random
import time
import pandas

cars_total = 0
last_update = time.time()

try:
    while True:
        
        # Randomizing
        if random.random() < 0.3:
            plate, time_a, time_b, speed = gen_one_car()
            cars_total += 1
            if speed > Speed_limit:
                status = "Speeding!!"
            else:
                status = "Good"
            print(f"Car #{cars_total} > {plate} going {speed} km/h >> {status}")
        
        # Wait for user to check output
        time.sleep(1 + random.random() * 2)
        
        # Check every 10 secs
        now = time.time()
        if now - last_update > 10:
            try:
                process()
                print("Results Updated.")

                read = pandas.read_csv(results_file)
                speeders = read[read['status'] == "High Speed"]

            except Exception:
                print("")

            last_update = now
except KeyboardInterrupt:
    print("\n\nRadar Turned Off")
    sys.exit