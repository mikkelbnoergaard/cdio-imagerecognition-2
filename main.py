from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
left_wheel = Motor(Port.B)
right_wheel = Motor(Port.A)
test_arm=Motor(Port.C)
robot = DriveBase(left_wheel,right_wheel, wheel_diameter= 55.5,axle_track=120)

# Write your program here

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
#test_arm.run(-500)
#robot.straight(500)

#left_wheel.run_target(800, -2000)æå++
#right_wheel.run_target(800, -2000)

def turn_360(robot, motor_speed):
  """
  This method turns the robot a full 360 degrees.

  Args:
      robot (DriveBase): The DriveBase object representing the robot.
      motor_speed (int): The speed at which the motors should turn (degrees per second).
  """
  # A full circle is 360 degrees
  turn_angle = 360

  # Use the DriveBase object's turn method for a controlled turn
  robot.turn(turn_angle, motor_speed)

# Call the method in your program

test_arm.run_target(300, -10000)

test_arm.run_target(800,10000)