#Simulates Radar data
import pandas
import random
from datetime import datetime, timedelta
from radar_conf import Distance

Num_cars = int(input("Give a number of cars: "))

# generateur mat
def gen_plate():    
    num = ""
    for i in range(6):
        num += str(random.randint(0,9))
    city = str(random.randint(1,58))
    letter = random.choice("ABDEFG")
    return num + "|" + city + "|" + letter

#main func
def data_gen():
    radar_a = []
    radar_b = []

    F_time = datetime.now().replace(microsecond=0)

    for i in range(Num_cars):
        plate = gen_plate()
       
        # Simulation a to b in random time
        seconds_a = random.randint(0, 300)
        time_a = F_time + timedelta(seconds=seconds_a)
        speed = random.randint(100, 200) #km/s
        
        time_seconds = (Distance / speed) * 3600

        time_b = time_a + timedelta(seconds=int(time_seconds))

        #making lists
        radar_a.append([plate, time_a])
        radar_b.append([plate, time_b])

        if i < 3:
            print(f"Car {i+1}: {plate} / speed: {speed} km/h")

    pandas.DataFrame(radar_a, columns=["plate", "time"]).to_csv("../Data/radar_a.csv", index=False)
    pandas.DataFrame(radar_b, columns=["plate", "time"]).to_csv("../Data/radar_b.csv", index=False)
    print("Files Edited")
data_gen()
