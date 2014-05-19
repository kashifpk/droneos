"""
Module to control a 4-servo quad copter
"""

import time
from motor import ServoMotor


class QuadCopter(object):
    """
    QuadCopter controller class
    """

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

    def hover(self):
        "Maintain current position and altitude"

        for servo in self.all_motors.values():
            servo.set_speed(50)

if '__main__' == __name__:

    m_FL = ServoMotor(4, "front-left")
    m_FR = ServoMotor(17, "front-right")
    m_RL = ServoMotor(22, "rear-left")
    m_RR = ServoMotor(27, "rear-right")

    drone = QuadCopter(m_FL, m_FR, m_RL, m_RR)

    drone.start()
    print("Ready for operation!!!")
    drone.hover()
    time.sleep(20)
    drone.stop()
