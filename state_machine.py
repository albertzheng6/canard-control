import time
import numpy as np
import sys
import pandas as pd

# A simulation for the state machine program for GNC
# There are 6 states during rocket flight. During each state, the corresponding code for that state and the state only
# runs in a loop, until a state transition has been detected.
#simulation data time step: 0.05 s

##### Setup #####
np.set_printoptions(threshold=sys.maxsize) # print entire array
#np.set_printoptions(threshold = False) # print truncated array
df = pd.read_csv('gnc_sim.csv') # convert csv file into dataframe
data = df.loc[:,:].to_numpy() # convert dataframe into numpy array
time_data = data[:,0]
time_steps = np.diff(time_data) # 1 unit shorter than time_data
alt_data = data[:,1]
accel_z_data = data[:,2]
ind = 0 # global variable that keeps track of time


def get_time(x):
    return time_data[x]
def get_alt(x):
    return alt_data[x]
def get_accel_z(x):
    return accel_z_data[x]

print("START OF FLIGHT")

##### 1.Pre-launch #####
print("Current state: Pre launch...")
while True:
    breakLoop = False

    # Detect state transition: liftoff
    count = 0
    accel_z = get_accel_z(ind)
    while accel_z >= 10:
        count = count + 1

        time.sleep(time_steps[ind])
        ind = ind + 1
        s1 = time_data[ind]
        s2 = alt_data[ind]
        s3 = accel_z_data[ind]
        print(f"{s1} s    {s2} m    {s3} m/s^2")

        if count >= 8:
            t = get_time(ind)
            print(f"Liftoff detected at {t} s")
            breakLoop = True
            break

        accel_z = get_accel_z(ind)

    if breakLoop == True:
        break

    time.sleep(time_steps[ind])
    ind = ind + 1
    s1 = time_data[ind]
    s2 = alt_data[ind]
    s3 = accel_z_data[ind]
    print(f"{s1} s    {s2} m    {s3} m/s^2")

##### 2.Powered ascent #####
print("Current state: Powered ascent...")
for x in range(0, 10): # delay to ensure initial negative accel z isnt captured
    time.sleep(time_steps[ind])
    ind = ind + 1
    s1 = time_data[ind]
    s2 = alt_data[ind]
    s3 = accel_z_data[ind]
    print(f"{s1} s    {s2} m    {s3} m/s^2")

while True:

    # Detect state transition: engine burnout
    accel_z = get_accel_z(ind)
    if accel_z < 0: # negative accel z -> engine burnout
        t = get_time(ind)
        print(f"Engine burnout detected at {t} s")
        break

    time.sleep(time_steps[ind])
    ind = ind + 1
    s1 = time_data[ind]
    s2 = alt_data[ind]
    s3 = accel_z_data[ind]
    print(f"{s1} s    {s2} m    {s3} m/s^2")

##### 3.Unpowered ascent #####
# State transition: detect apogee
print("Current state: Unpowered ascent...")
old_alt = get_alt(ind)
while True:

    # Detect state transition: apogee

    for x in range(0,10):
        time.sleep(time_steps[ind])
        ind = ind + 1
        s1 = time_data[ind]
        s2 = alt_data[ind]
        s3 = accel_z_data[ind]
        print(f"{s1} s    {s2} m    {s3} m/s^2")

    current_alt = get_alt(ind)
    if current_alt < old_alt:
        apogee = current_alt
        t = get_time(ind)
        print(f"Apogee detected at {t} s")
        break

    old_alt = current_alt

##### 4.Free fall #####
# State transition: detect pyro fire
print("Current state: Free fall")
while True:

    # Detect state transition: chute deployment

    time.sleep(time_steps[ind])
    ind = ind + 1
    s1 = time_data[ind]
    s2 = alt_data[ind]
    s3 = accel_z_data[ind]
    print(f"{s1} s    {s2} m    {s3} m/s^2")

    alt = get_alt(ind)
    if alt < apogee:
        t = get_time(ind)
        print(f"Chutes deployed at {t} s")
        break


##### 5.Chute descent #####
print("Current state: Chute descent")
while True:

    time.sleep(time_steps[ind])
    ind = ind + 1
    s1 = time_data[ind]
    s2 = alt_data[ind]
    s3 = accel_z_data[ind]
    print(f"{s1} s    {s2} m    {s3} m/s^2")

    # Detect state transition: landing
    alt = get_alt(ind)
    accel_z = get_accel_z(ind)
    if (accel_z >= -1 and accel_z <= 1) or (alt < 10):
        t = get_time(ind)
        print(f"Landing detetected at {t} s")
        break

##### 6.Landing: rocket has landed #####
print("END OF FLIGHT")
