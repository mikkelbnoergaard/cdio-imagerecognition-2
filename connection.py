#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

ev3 = EV3Brick()

left_wheel = Motor(Port.B)
right_wheel = Motor(Port.A)
test_arm=Motor(Port.C)
robot = DriveBase(left_wheel,right_wheel, wheel_diameter= 55.5,axle_track=120)



def turn_360(robot, motor_speed):
  # A full circle is 360 degrees
  turn_angle = 360

  # Use the DriveBase object's turn method for a controlled turn
  robot.turn(turn_angle, motor_speed)

# Call the method in your program

# test_arm.run_target(300, -10000)

# test_arm.run_target(800,10000)


import time


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

eatBalls = True

while True:
    # Establish a connection
    clientsocket,addr = serversocket.accept()
    
    # Receive the command
    command = clientsocket.recv(1024).decode('utf-8')

    if eatBalls:
        test_arm.run(-500)
    
    if command == 'FORWARD':
        left_wheel.run(200)
        right_wheel.run(200)
        time.sleep(0.2)
        left_wheel.stop()
        right_wheel.stop()
    elif command == 'BACKWARD':
        left_wheel.run(300)
        right_wheel.run(300)
        time.sleep(0.7)
        left_wheel.stop()
        right_wheel.stop()
    elif command == 'LEFT':
        left_wheel.run(-200)
        right_wheel.run(200)
        time.sleep(0.2)
        left_wheel.stop()
        right_wheel.stop()
    elif command == 'RIGHT':
        right_wheel.run(-200)
        left_wheel.run(200)
        time.sleep(0.2)
        right_wheel.stop()
        left_wheel.stop()
    elif command == 'ARM_IN':
        right_wheel.run(-200)
        left_wheel.run(-200)
        time.sleep(0.2)
        right_wheel.stop()
        left_wheel.stop()
    elif command == 'ARM_OUT':
        left_wheel.stop()
        right_wheel.stop()
        test_arm.stop()
        time.sleep(0.5)
        eatBalls = False
        test_arm.run(2000)
    elif command == 'STOP':
        left_wheel.stop()  # Stop the left wheel
        right_wheel.stop()  # Stop the right wheel
        test_arm.stop()  # Stop the test arm
    elif command == 'NAVIGATE_LEFT':
        left_wheel.run(-200)
        time.sleep(0.2)
        left_wheel.run(100)
        right_wheel.run(200)
        time.sleep(0.2)
        left_wheel.stop()
        right_wheel.stop()
    elif command == 'NAVIGATE_RIGHT':
        right_wheel.run(-200)
        time.sleep(0.2)
        right_wheel.run(100)
        left_wheel.run(200)
        time.sleep(0.2)
        right_wheel.stop()
        left_wheel.stop()

    clientsocket.close()
