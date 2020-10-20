# -*- coding: utf-8 -*-
"""
CLI to interact with the New Focus Open-Loop Picomotor Controller via Telnet
(Luis R. 2015)
"""

host = "192.168.1.13"

import telnetlib
import time

def get_drive():
    """
    ask user which drive of the controller should be used
    return its index
    """
    drive_input = input("Which drive: 1 or 2? ")
    while (drive_input != "1") and (drive_input != '2'):
        drive_input = input("This drive does not exist. Pick drive 1 or 2: ")
    drive = int(drive_input)
    return drive

def get_motor():
    """
    ask user which motor port of the selected drive of the controller should be used
    return its index
    """
    motor_set = 0
    while not motor_set:
        motor_input = input("Which motor: a, b, or c? ")
        if motor_input=='0' or motor_input=='a' or motor_input=='A':
            motor_set = 1
            motor = 0
        elif motor_input=='1' or motor_input=='b' or motor_input=='B':
            motor_set = 1
            motor = 1
        elif motor_input=='2' or motor_input=='c' or motor_input=='C':
            motor_set = 1
            motor = 2
        else: print('This motor does not exist.')
    return motor

def get_steps():
    """
    ask user how many steps the selected motor should do
    return the number of steps
    """
    steps_set = 0
    while not steps_set:
        try:
            steps_input = int(input("How many steps (pos. or neg. integer)? "))
            steps = steps_input
            steps_set = 1
        except ValueError:
            print("Not a valid positive or negative integer.")
    return steps
    
def get_movement_params():
    """
    ask for all movement parameters
    """
    drive = get_drive()
    motor = get_motor()
    steps = get_steps()            
    return (drive,motor,steps)

def print_movement_info(drive,motor,steps):
    print("New movement parameters: drive " + str(drive) + ", motor " + str(motor) + ", steps " + str(steps))
    
def do_movement(drive,motor,steps):
    """
    sends a movement command to the controller via Telnet
    """
    tn = telnetlib.Telnet(host)
    
    def wait():
        delay = 0.1
        time.sleep(delay)
        
    def move_relative(drive,motor,steps):
        tn.write(b"chl a" + str(drive).encode('ascii') + b"=" + str(motor).encode('ascii') + b"\n")
        wait()
        tn.write(b"rel a" + str(drive).encode('ascii') + b"=" + str(steps).encode('ascii') + b"\n")
        wait()
        tn.write(b"go\n")
        wait()
        
    move_relative(drive,motor,steps)
    
    tn.close()
    
    print("  -------> MOVEMENT DONE: drive " + str(drive) + ", motor " + str(motor) + ", steps " + str(steps))    


    
print("***************************************************")    
print("**         Picomotor control interface           **")
print("***************************************************")

(drive,motor,steps) = get_movement_params()
print_movement_info(drive,motor,steps)

loop = True
while(loop):
    nextstep = input("go [g], change no. of steps [s], change all movement parameters [p], or exit [q]? ")
    if nextstep == 'g':
        loop = True
        do_movement(drive,motor,steps)
    elif nextstep == 'p':
        loop = True
        (drive,motor,steps) = get_movement_params()
        print_movement_info(drive,motor,steps)    
    elif nextstep == 's':
        loop = True
        steps = get_steps()
        print_movement_info(drive,motor,steps)
    elif nextstep == 'q':
        loop = False
    else: 
        print("Invalid answer.")        
        loop = True