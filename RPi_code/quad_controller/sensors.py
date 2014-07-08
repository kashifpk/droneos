"""
Sensors like accelerometer and gyro interface classes for use with RPi
"""

import smbus
import math
import time
from threading import Thread


def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


class AcceleroGryroSensor(object):
    """
    Class for taking readings from MPU-6050 Six-Axis Gyro + Accelerometer sensor
    """

    POWER_MGMT_1 = 0x6b
    POWER_MGMG_2 = 0x6c

    GYRO_SCALE = 131.0
    ACCEL_SCALE = 16384.0

    READ_FREQUENCY = 0.01

    # This is the address value read via the i2cdetect command
    SENSOR_ADDRESS = 0x68

    is_sensing = False  # set this flag to to False to stop sensing

    def __init__(self, bus_num=1):
        """
        bus_num is 0 for RPi Rev 1 boards and 1 (default) for Rev. 2 boards
        """

        self.bus = smbus.SMBus(bus_num)

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.SENSOR_ADDRESS, self.POWER_MGMT_1, 0)

        self._gyro_scaled_x = 0
        self._gyro_scaled_y = 0
        self._gyro_scaled_z = 0

        self._accel_scaled_x = 0
        self._accel_scaled_y = 0
        self._accel_scaled_z = 0

        self.x_offset = 0
        self.y_offset = 0

        self.rotation_x = 0    # last X rotation
        self.rotation_y = 0    # last Y rotation

    def read_all(self):
        "Reads both gyro and accelero data and sets internal properties"

        raw_gyro_data = self.bus.read_i2c_block_data(self.SENSOR_ADDRESS,
                                                     0x43, 6)
        raw_accel_data = self.bus.read_i2c_block_data(self.SENSOR_ADDRESS,
                                                      0x3b, 6)

        self._gyro_scaled_x = twos_compliment(
            (raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.GYRO_SCALE
        self._gyro_scaled_y = twos_compliment(
            (raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.GYRO_SCALE
        self._gyro_scaled_z = twos_compliment(
            (raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.GYRO_SCALE

        self._accel_scaled_x = twos_compliment(
            (raw_accel_data[0] << 8) + raw_accel_data[1]) / self.ACCEL_SCALE
        self._accel_scaled_y = twos_compliment(
            (raw_accel_data[2] << 8) + raw_accel_data[3]) / self.ACCEL_SCALE
        self._accel_scaled_z = twos_compliment(
            (raw_accel_data[4] << 8) + raw_accel_data[5]) / self.ACCEL_SCALE

    def set_offsets(self, x_offset=None, y_offset=None):
        "Sets any offsets for sensor positioning"

        self.read_all()

        if not x_offset:
            x_offset = self._gyro_scaled_x

        if not y_offset:
            y_offset = self._gyro_scaled_y

        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_rotation(self):
        "Returns current sensor X,Y rotation"

        self.read_all()
        last_x = get_x_rotation(self._accel_scaled_x,
                                self._accel_scaled_y,
                                self._accel_scaled_z)

        last_y = get_y_rotation(self._accel_scaled_x,
                                self._accel_scaled_y,
                                self._accel_scaled_z)

        self.rotation_x = last_x - self.x_offset
        self.rotation_y = last_y - self.y_offset

        return dict(x_rot=self.rotation_x, y_rot=self.rotation_y)

    def start_sensing(self):
        """
        Meant to be called as a separate thread,
        keeps sensing according to READ_FREQUENCY
        """

        self.is_sensing = True

        # K + K1 should be == 1
        K = 0.98
        K1 = 1 - K

        gyro_total_x = (self.rotation_x) - self.x_offset
        gyro_total_y = (self.rotation_y) - self.y_offset

        while self.is_sensing:
            time.sleep(self.READ_FREQUENCY - 0.005)

            self.read_all()

            self._gyro_scaled_x -= self.x_offset
            self._gyro_scaled_y -= self.y_offset

            gyro_x_delta = (self._gyro_scaled_x * self.READ_FREQUENCY)
            gyro_y_delta = (self._gyro_scaled_y * self.READ_FREQUENCY)

            gyro_total_x += gyro_x_delta
            gyro_total_y += gyro_y_delta

            rotation_x = get_x_rotation(self._accel_scaled_x,
                                        self._accel_scaled_y,
                                        self._accel_scaled_z)

            rotation_y = get_y_rotation(self._accel_scaled_x,
                                        self._accel_scaled_y,
                                        self._accel_scaled_z)

            self.rotation_x = K * (self.rotation_x + gyro_x_delta) + (K1 * rotation_x)
            self.rotation_y = K * (self.rotation_y + gyro_y_delta) + (K1 * rotation_y)


if '__main__' == __name__:

    gyro = AcceleroGryroSensor()
    gyro.set_offsets(-1, 7.5)

    sensing_thread = Thread(target=AcceleroGryroSensor.start_sensing, args=(gyro,))

    try:
        sensing_thread.start()
        while True:
            print("Rot X: {0}, Rot Y: {1}".format(gyro.rotation_x, gyro.rotation_y))
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        gyro.is_sensing = False

    sensing_thread.join()
    print("Finished!")
