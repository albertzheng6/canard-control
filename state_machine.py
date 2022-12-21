import time

# A simulation for the state machine program for GNC
# There are 6 states during rocket flight. During each state, the corresponding code for that state and the state only
# runs in a loop, until a state transition has been detected.

def get_accel_z():
    # get current accel z
    print('accel_z: ')
    x = int(input())
    return x

def get_alt():
    # get current altitude
    print('get_alt: ')
    x = int(input())
    return x

# 1. Pre launch - rocket sitting on launchpad
print("Current state: Pre launch...")
while True:
    breakLoop = False

    # Detect state transition: liftoff
    count = 0
    accel_z = get_accel_z()
    while accel_z >= 5:
        count = count + 1
        time.sleep(0.1)
        if count >= 2:
            print("Liftoff detected")
            breakLoop = True
            break

        accel_z = get_accel_z()

    if breakLoop == True:
        break

# 2. Powered flight - rocket under
print("Current state: Powered flight...")
while True:
    breakLoop = False

    # Run control algo

    # Detect state transition: engine burnout
    count = 0
    accel_z = get_accel_z()
    while accel_z <= 2:
        count = count + 1
        time.sleep(0.1)
        if count >= 2:
            print("Engine burnout detected")
            breakLoop = True
            break

        accel_z = get_accel_z()

    if breakLoop == True:
        break

# 3. Unpowered flight
# State transition: detect apogee
print("Current state: Unpowered flight...")
old_alt = get_alt()
while True:

    time.sleep(1)  # wait 1 sec
    current_alt = get_alt()

    if current_alt < old_alt:
        print("Apogee detected")
        break

    old_alt = current_alt



# 4. Free fall
# State transition: detect pyro fire
print("Current state: Free fall")
while True:

    alt = get_alt()

    if alt < 25:
        print("Chutes deployed")
        break



# 5. Chute descent
# State transition: detect landing
print("Current state: Chute descent")
while True:

    accel_z = get_accel_z()
    if accel_z >= -1 and accel_z <= 1:
        print("Landing")
        break

# 6. Landing: rocket has landed
