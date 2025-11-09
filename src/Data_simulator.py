#Simulates Radar data
import pandas
import random
import os
from datetime import datetime, timedelta
from radar_conf import Distance, Num_cars, radar_a_file, radar_b_file

# generateur mat
def gen_plate():    
    num = ""
    for i in range(6):
        num += str(random.randint(0,9))
    city = str(random.randint(1,58))
    letter = random.choice("ABDEFG")
    return num + "|" + letter + "|" + city

def add_to_csv(file, stuff):
    os.makedirs(os.path.dirname(file), exist_ok=True)

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
    time_b = time_a + timedelta(seconds=int(time_seconds) + random.randint(-1,1))

    add_to_csv(radar_a_file, [plate, time_a])
    add_to_csv(radar_b_file, [plate, time_b])

    return plate, time_a, time_b, speed