#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

left_wheel = Motor(Port.B)
right_wheel = Motor(Port.A)
test_arm=Motor(Port.C)
robot = DriveBase(left_wheel,right_wheel, wheel_diameter= 55.5,axle_track=120)

### Example Code

#### EV3 Brick (MicroPython)
# This is a simplified example. Your implementation might differ.
import socket

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = "0.0.0.0"
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

while True:
    # Establish a connection
    clientsocket,addr = serversocket.accept()
    
    # Receive the command
    command = clientsocket.recv(1024).decode('utf-8')
    
    if command == 'FORWARD':
        test_arm.run_target(1000, -10000000)
        pass
    elif command == 'BACKWARD':
        # Code to move the robot backward
        pass

    clientsocket.close()



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.



# Write your program here.

