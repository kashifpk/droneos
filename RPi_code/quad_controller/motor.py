"""
Motor Controller module using Raspberry Pi's PWM Servo controller
"""
#Derived from code by: solenero.tech@gmail.com

from RPIO import PWM


class ServoMotor(object):
    """
    Servo Brushless Motor controller class
    """

    def __init__(self, pin, name, kv_multiplier=1000, min_granularity=0, max_granularity=100):

        self.pin = pin
        self.name = name
        self.kv_multiplier = kv_multiplier
        self.min_granularity = min_granularity
        self.max_granularity = max_granularity
        self.current_speed = 0
        self.powered = False

    def __str__(self):
        return "<%s (Pin: %i): %i>" % (self.name, self.pin, self.current_speed)


    def start(self):
        "Run the procedure to init the PWM"

        self.__IO = PWM.Servo()
        self.powered = True


    def stop(self):
        "Stop PWM signal"

        self.set_speed(0)
        if self.powered:
            self.__IO.stop_servo(self.pin)
            self.powered = False

    def set_speed(self, speed):
        "Set pulse 1-100 for the motor"

        self.current_speed = speed

        pwm = speed
        if pwm < self.min_granularity:
            pwm = self.min_granularity
        elif pwm > self.max_granularity:
            pwm = self.max_granularity

        pwm = (self.kv_multiplier + (pwm * 10))
        # Set servo to xxx us
        if self.powered:
            self.__IO.set_servo(self.pin, pwm)



