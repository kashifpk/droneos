import RPi.GPIO as GPIO
import sys
import time


class PWM(object):
    """
    PWM (Pulse Width Modulation) generator and manager class
    """

    pulse_generators = []

    def __init__(self):
        "Constructor - Sets up GPIO mode to BCM"

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

    def __del__(self):
        "Destructor - Cleans up any pin assignments"

        GPIO.cleanup()

    def __str__(self):
        "A human readable representation of current state"

        return "PWM([%r])" % self.pulse_generators

    def add_pulse_generator(self, specs_str):
        """
        Adds a pulse generator, takes pulse specs string of the format::

        pin:clock_duration:pulse_duration
        """

        pin, clock_duration, pulse_duration = specs_str.split(':')
        pulse_dict = {'pin': int(pin),
                      'clock': float(clock_duration),
                      'pulse': float(pulse_duration)}

        self.pulse_generators.append(pulse_dict)
        GPIO.setup(int(pin), GPIO.OUT)

    def start(self):
        "Starts generating pulses for the pulse generators currently present"

        if not self.pulse_generators:
            return

        pulse = self.pulse_generators[0]

        on_sleep_time = pulse['pulse'] * pulse['clock']
        off_sleep_time = pulse['clock'] - on_sleep_time

        while True:
            try:
                GPIO.output(pulse['pin'], 1)
                time.sleep(on_sleep_time)

                GPIO.output(pulse['pin'], 0)
                time.sleep(off_sleep_time)

            except (KeyboardInterrupt, SystemExit):
                break
            except Exception, exp:
                print(exp)

if '__main__' == __name__:
    usage = """
    Syntax:

        %s pin:clock_duration:pulse_duration [pin:clock_duration:pulse_duration] ...

    Example:

        %s 18:1:0.5

        # set half second pulse for each second on pin 18 (according to RPi BCM layout)


        %s 18:1:0.25 23:1:0.5 24:0.5:0.2

        # 1/4th second pulse on pin 18 for each second,
        # half second pulse on pin 23 for each second
        # 20 percent of half second (results in 1/10th of a second) pulse on pin 24

        """ % (sys.argv[0], sys.argv[0], sys.argv[0])

    if len(sys.argv) < 2:
        print(usage)
        sys.exit()

    pwm = PWM()

    for pwm_str in sys.argv[1:]:
        pwm.add_pulse_generator(pwm_str)

    print(pwm)
    pwm.start()
