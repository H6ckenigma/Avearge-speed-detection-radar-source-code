This project simulates a radar speed detection system. The idea is that two radar points, A and B, detect a car’s license plate as it passes by. The system records the exact time when the car is seen at each point, then calculates the average speed based on the distance between the two radars and the time difference and if the calculated speed is higher than the allowed speed limit, the system automatically flags it as overspeeding (High Speed in the code so far) case

Since It's illegal to record a real highway, I simulated random data (license plates and timestamps and speeds) using a python script called Data_simulation.py and this allows me to test the algorithm and demonstrate how the detection and speed calculation process works.

