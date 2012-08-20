#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of using single pin IO objects to output to GPIO pins.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import time
import sys
if __name__ == '__main__':
    sys.path.insert(0, './..')
import dibase.rpi.gpio.pin as pin
import dibase.rpi.gpio.gpioerror as error

if __name__ == '__main__':
    try:
        with pin.open_pin( pin.PinId.p1_gpio_gen1(), 'w' ) as out_pin:
            out_pin.write(True)     # Set GPIO line on pin p1_gpio_gen1 HIGH
            time.sleep(0.2)
            out_pin.write(False)    # Set GPIO line on pin p1_gpio_gen1 LOW
            time.sleep(0.2)
            out_pin.write(1)        # Set GPIO line on pin p1_gpio_gen1 HIGH
            time.sleep(0.2)
            out_pin.write(0)        # Set GPIO line on pin p1_gpio_gen1 LOW
            time.sleep(0.2)
            out_pin.write(23)       # Set GPIO line on pin p1_gpio_gen1 HIGH
            time.sleep(0.2)
            out_pin.write(None)     # Set GPIO line on pin p1_gpio_gen1 LOW
            time.sleep(0.2)
            out_pin.write('1')      # Set GPIO line on pin p1_gpio_gen1 HIGH
            time.sleep(0.2)
            out_pin.write('0')      # Set GPIO line on pin p1_gpio_gen1 LOW
            time.sleep(0.2)

    except error.GPIOError, e:
        print "Oops unexpected GPIO related error:",\
                e.__class__.__name__,':', e
    except ValueError:
        print "Oops unexpected value error!"
