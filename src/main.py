# Main : Error Handling and Perfecting
import time
import os
import sys

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
        print("Everything is good!")
        time.sleep(1)
files_check()
