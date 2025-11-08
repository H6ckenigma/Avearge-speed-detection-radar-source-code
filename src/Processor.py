# Speed Calculation and Overall logic
import pandas
from datetime import datetime
from radar_conf import Distance, Speed_limit

# Moroccan Cities
citys = {"1": "Rabat", "2": "Salé Medina", "3": "Sala El-jadida", "4": "Skhirat - Témara", "5": "Khémissat", "6": "Casablanca 1", "7": "Casablanca 2", "8": "Casablanca 3", "9": "Casablanca 4", "10": "Casablanca 5", "11": "Casablanca 6", "12": "Casablanca 7", "13": "Casablanca 8", "14": "Mohammadia", "15": "Fès 1", "16": "Fès 2", "17": "Fès 3", "18": "Sefrou", "19": "Boulmane", "20": "Meknès 1", "21": "Meknès 2", "22": "El Hajeb", "23": "Ifrane", "24": "Khénifra", "25": "Errachidia", "26": "Marrakesh 1", "27": "Marrakech 2", "28": "Marrakesh 3", "29": "Marrakesh 4", "30": "Chichaoua", "31": "Kelaat sraghna", "32": "Essaouira", "33": "Agadir", "34": "Inezgane", "35": "Chtouka","36": "Taroudant","37": "Tiznit","38": "Ouarzazate","39": "Zagora","40": "Tanger","41": "Beni mekada","42": "Laarache","43": "Chefchaouen","44": "Tétouan","45": "El hoceïma","46": "Taza","47": "Taounate","48": "Oujda","49": "Berkane","50": "Nador","51": "Taourirt","52": "Jerada","53": "Figuig","54": "Safi","55": "El jadida","56": "Settat","57": "Khouribga","58": "Benslimane" }

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
    merged['city_code'] = merged['plate'].str.split('|').str[2]
    merged['city'] = merged['city_code'].map(citys).fillna("Unknown")
    
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
        bad = bad.sort_values(by='excess', ascending=False)
        print("The cars that has exceeded the limit are")
        print(bad[['plate', 'speed', 'excess', 'status', 'city']])
    else:
        print("All drivers are Good")
process()