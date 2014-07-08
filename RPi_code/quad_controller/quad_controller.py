"""
Module to control a 4-servo quad copter
"""

import time
from threading import Thread
from motor import ServoMotor
from sensors import AcceleroGryroSensor


class QuadCopter(object):
    """
    QuadCopter controller class
    """

    short_names = {"FL": "front_left",
                   "FR": "front_right",
                   "RL": "rear_left",
                   "RR": "rear_right"}

    MAX_ANGLE = 30   # maximum X or Y tilt angle that is allowed for the QC
    ANGLE_TOLERANCE = 1  # maximum angle tolerance when QC stops adjusting

    def __init__(self, m_front_left, m_front_right, m_rear_left, m_rear_right):
        """
        Takes 4 Servo motor objects
        """

        self.sensor = AcceleroGryroSensor()
        self.sensing_thread = None

        self.m_front_left = m_front_left
        self.m_front_right = m_front_right
        self.m_rear_left = m_rear_left
        self.m_rear_right = m_rear_right
        self.all_motors = {'front_left': self.m_front_left,
                           'front_right': self.m_front_right,
                           'rear_left': self.m_rear_left,
                           'rear_right': self.m_rear_right}

    def setup_ESCs(self):
        "setup motor controllers"

        print("!!!!!! MOTORS SETUP !!!!!!")
        print('***Disconnect ESC power')
        print('***then press ENTER')
        raw_input()
        for servo in self.all_motors.values():
            servo.start()
            servo.set_speed(100)

        print('***Connect ESC Power')
        print('***Wait beep-beep')

        print('***then press ENTER')
        raw_input()
        for servo in self.all_motors.values():
            servo.set_speed(0)

        print('***Wait N beep for battery cell')
        print('***Wait beeeeeep for ready')
        print('***then press ENTER')
        raw_input()

    def setup_gyro(self):
        "Setup accelero and gryo sensor"

        print("!!!!!! GYRO SETUP !!!!!!")
        print("Place the copter in a flat balanced surface and press enter")
        raw_input()
        self.sensor.set_offsets(-3.5, 10)
        print("X offset: {0}, Y offset: {1}".format(
            self.sensor.x_offset, self.sensor.y_offset))

    def start(self):
        "Start quadcopter - starts all motors"

        self.setup_gyro()
        self.setup_ESCs()
        self.sensing_thread = Thread(
            target=AcceleroGryroSensor.start_sensing, args=(self.sensor, ))
        self.sensing_thread.start()

    def stop(self):
        "Stop quadcopter - stops all motors"

        self.sensor.is_sensing = False
        self.sensing_thread.join()

        for servo in self.all_motors.values():
            servo.stop()

    def set_speed(self, new_speed, target_motor_names):
        """
        Sets speed of one or multiple motors. Example calls::

            set_speed(50, "FL,FR")
            set_speed(40, "ALL")
            set_speed(75, "RL")

        FL = Front Left
        FR = Front Right
        RL = Rear Left
        RR = Rear Right
        ALL = All motors
        """

        if "ALL" == target_motor_names:
            for servo in self.all_motors.values():
                servo.set_speed(new_speed)
        else:
            m_names = target_motor_names.split(',')
            for m_name in m_names:
                real_name = self.short_names[m_name]
                servo = self.all_motors[real_name]
                servo.set_speed(new_speed)

    def __str__(self):

        ret = "Rot X: {0}, Rot Y: {1}, Offset X,Y: {2},{3}\n\n".format(
            self.sensor.rotation_x, self.sensor.rotation_y,
            self.sensor.x_offset, self.sensor.y_offset)

        for servo in self.all_motors.values():
            ret += str(servo) + "\n"

        return ret

    def hover(self):
        "Maintain current position and altitude"

        self.set_speed(50, "ALL")

    def maintain_vector(self, average_speed, x_angle, y_angle):
        """
        Tries to maintain the given angles and average speed.
        Adjusts motor speeds and attempts to reach the given
        angles and speed
        """

        # get current x and y angles
        current_x = self.sensor.rotation_x
        current_y = self.sensor.rotation_y

        new_x = x_angle - current_x
        new_y = y_angle - current_y

        FLx, FLy, FRx, FRy, RLx, RLy, RRx, RRy = [0, 0, 0, 0, 0, 0, 0, 0]

        adjust_x = False
        adjust_y = False

        if abs(new_x) > self.ANGLE_TOLERANCE:

            adjust_x = True
            step = abs(int(new_x/2))

            if new_x > 0:
                # +(FL & RL), -(FR, RR)
                FLx = average_speed + step
                RLx = average_speed + step
                FRx = average_speed - step
                RRx = average_speed - step

            elif new_x < 0:
                # -(FL & RL), +(FR, RR)
                FLx = average_speed - step
                RLx = average_speed - step
                FRx = average_speed + step
                RRx = average_speed + step

        if abs(new_y) > self.ANGLE_TOLERANCE:

            adjust_y = True
            step = abs(int(new_y/2))

            if new_y > 0:
                # +(RR & RL), -(FR, FL)
                FLy = average_speed - step
                FRy = average_speed - step
                RLy = average_speed + step
                RRy = average_speed + step

            elif new_y < 0:
                # -(RR & RL), +(FR, FL)
                FLy = average_speed + step
                FRy = average_speed + step
                RLy = average_speed - step
                RRy = average_speed - step

        if adjust_x and adjust_y:
            self.m_front_left.set_speed((FLx + FLy) / 2)
            self.m_front_right.set_speed((FRx + FRy) / 2)
            self.m_rear_left.set_speed((RLx + RLy) / 2)
            self.m_rear_right.set_speed((RRx + RRy) / 2)

        elif adjust_x:
            self.m_front_left.set_speed(FLx)
            self.m_front_right.set_speed(FRx)
            self.m_rear_left.set_speed(RLx)
            self.m_rear_right.set_speed(RRx)

        elif adjust_y:
            self.m_front_left.set_speed(FLy)
            self.m_front_right.set_speed(FRy)
            self.m_rear_left.set_speed(RLy)
            self.m_rear_right.set_speed(RRy)

        #print("maintain_vector: CX: {0}, CY: {1}; NX: {2}, NY: {3};".format(
        #    current_x, current_y, new_x, new_y))
        #print("FLx: {0}, FLy: {1}; FRx: {2}, FRy: {3}; RLx: {4}, RLy: {5}; RRx: {6}, RRy: {7};".format(
        #    FLx, FLy, FRx, FRy, RLx, RLy, RRx, RRy))


if '__main__' == __name__:

    menu = """
    Set Speed:

        speed motor_names

    FL = Front Left
    FR = Front Right
    RL = Rear Left
    RR = Rear Right
    ALL = All motors

    press q and enter to Quit

"""
    m_FL = ServoMotor(18, "front-left")
    m_FR = ServoMotor(23, "front-right")
    m_RL = ServoMotor(24, "rear-left")
    m_RR = ServoMotor(25, "rear-right")

    drone = QuadCopter(m_FL, m_FR, m_RL, m_RR)

    drone.start()
    print("Ready for operation!!!")

    choice = None
    while True:
        print(menu)
        choice = raw_input("Your choice > ")

        if 'q' == choice.lower().strip():
            break
        elif ' ' in choice:
            parts = choice.upper().strip().split(' ')
            speed = int(parts[0])
            motor_names = parts[1]
            drone.set_speed(speed, motor_names)
            print(drone)
        else:
            print("    <Invalid choice>")

    #drone.hover()
    #time.sleep(20)
    drone.stop()
    time.sleep(2)
