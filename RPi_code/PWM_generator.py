import RPi.GPIO as GPIO
import sys
import time
from fractions import gcd


def get_min_sleep_interval(pulses_list):
    plist2 = [int(i*1000) for i in pulses_list]
    res = reduce(gcd, plist2)
    return res/1000.0


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

        pulses_list = [i['pulse'] * i['clock'] for i in self.pulse_generators]
        min_pulse = get_min_sleep_interval(pulses_list)

        pin_states = {}
        for pulse in self.pulse_generators:
            on_time = pulse['pulse'] * pulse['clock']
            off_time = pulse['clock'] - on_time

            pin_states[pulse['pin']] = dict(off_time=off_time,
                                            on_time=on_time,
                                            current_status='off',
                                            current_state_duration=0.0)

        while True:
            time.sleep(min_pulse)

            try:
                for pulse in self.pulse_generators:

                    pin = pulse['pin']
                    status = pin_states[pin]['current_status']
                    pin_states[pin]['current_state_duration'] += min_pulse

                    if 'off' == status:

                        if pin_states[pin]['current_state_duration'] >= pin_states[pin]['off_time']:
                            # Turn the pin ON
                            GPIO.output(pulse['pin'], 1)
                            pin_states[pin]['current_status'] = 'on'
                            pin_states[pin]['current_state_duration'] = 0.0

                    elif 'on' == status:

                        if pin_states[pin]['current_state_duration'] >= pin_states[pin]['on_time']:
                            # Turn the pin ON
                            GPIO.output(pulse['pin'], 0)
                            pin_states[pin]['current_status'] = 'off'
                            pin_states[pin]['current_state_duration'] = 0.0

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
