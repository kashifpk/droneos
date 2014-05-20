"""
Module to control a 4-servo quad copter
"""

import time
from motor import ServoMotor


class QuadCopter(object):
    """
    QuadCopter controller class
    """

    short_names = {"FL": "front_left",
                   "FR": "front_right",
                   "RL": "rear_left",
                   "RR": "rear_right"}

    def __init__(self, m_front_left, m_front_right, m_rear_left, m_rear_right):
        """
        Takes 4 Servo motor objects
        """

        self.m_front_left = m_front_left
        self.m_front_right = m_front_right
        self.m_rear_left = m_rear_left
        self.m_rear_right = m_rear_right
        self.all_motors = {'front_left': self.m_front_left,
                           'front_right': self.m_front_right,
                           'rear_left': self.m_rear_left,
                           'rear_right': self.m_rear_right}

    def start(self):
        "Start quadcopter - starts all motors"

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

    def stop(self):
        "Stop quadcopter - stops all motors"

        for servo in self.all_motors.values():
            servo.stop()

    def set_speed(self, new_speed, motor_names):
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

        if "ALL" == motor_names:
            for servo in self.all_motors.values():
                servo.set_speed(new_speed)
        else:
            m_names = motor_names.split(',')
            for m_name in m_names:
                real_name = self.short_names[m_name]
                servo = self.all_motors[real_name]
                servo.set_speed(new_speed)

    def __str__(self):

        ret = ""

        for servo in self.all_motors.values():
            ret += str(servo) + "\n"

        return ret

    def hover(self):
        "Maintain current position and altitude"

        self.set_speed(50, "ALL")


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
    m_FL = ServoMotor(4, "front-left")
    m_FR = ServoMotor(17, "front-right")
    m_RL = ServoMotor(22, "rear-left")
    m_RR = ServoMotor(27, "rear-right")

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
