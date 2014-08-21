from quad_controller import QuadCopter
from motor import ServoMotor
import time

if __name__ == '__main__':
    m_FL = ServoMotor(4, "front-left")
    m_FR = ServoMotor(17, "front-right")
    m_RL = ServoMotor(22, "rear-left")
    m_RR = ServoMotor(27, "rear-right")

    drone = QuadCopter(m_FL, m_FR, m_RL, m_RR)
    drone.start()
    print("Ready for operation!!!")

    # flying 
    drone.set_speed(60, "ALL")
    time.sleep(5)

    # landing
    drone.set_speed(45, "ALL")
    drone.set_speed(43, "ALL")
    drone.set_speed(40, "ALL")
    drone.set_speed(38, "ALL")
    drone.set_speed(30, "ALL")
    drone.set_speed(20, "ALL")
    drone.set_speed(0, "ALL")

    drone.stop()
    time.sleep(2)
    