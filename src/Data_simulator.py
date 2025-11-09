#Simulates Radar data
import pandas
import random
import os
from datetime import datetime, timedelta
from radar_conf import Distance, Num_cars

# generateur mat
def gen_plate():    
    num = ""
    for i in range(6):
        num += str(random.randint(0,9))
    city = str(random.randint(1,58))
    letter = random.choice("ABDEFG")
    return num + "|" + letter + "|" + city

def add_to_csv(file, stuff):
    df = pandas.DataFrame([stuff], columns=["plate", "time"])
    if os.path.exists(file):
        df.to_csv(file, mode='a', header=False, index=False)
    else:
        df.to_csv(file, index=False)

    # Generate Only One Car
    def gen_one_car():
        plate = gen_plate()

        now = datetime.now()
        offset = random.randint(-5, 5)
        time_a = now + timedelta(seconds=offset)

        speed = random.randint(80, 160)

        time_seconds = (Distance / speed) * 3600
        time_b = time_a + timedelta(seconds=int(time_seconds))

        add_to_csv("../data/radar_a.csv", [plate, time_a])
        add_to_csv("../data/radar_b.csv", [plate, time_b])

        return plate, time_a, time_b