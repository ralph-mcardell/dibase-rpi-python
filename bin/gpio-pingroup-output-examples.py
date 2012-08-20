#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of using multiple pins IO objects to output to GPIO pins.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import time
import sys
if __name__ == '__main__':
    sys.path.insert(0, './..')
import dibase.rpi.gpio.pingroup as pingroup
import dibase.rpi.gpio.gpioerror as error

def toggle_gpio_gen0_gen1_integer():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()
                                 , pingroup.PinId.p1_gpio_gen1()
                                 ]
                               , 'wI') as out_pins:
        out_pins.write(3)     # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write(0)     # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write('3')   # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write('0')   # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write(3.1)   # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write(0.0)   # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write(1 | 2) # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write(False) # Set both pin group GPIO pins LOW
        time.sleep(0.2)

def cycle_gpio_gen0_gen1_integer():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()
                                 , pingroup.PinId.p1_gpio_gen1()
                                 ]
                               , 'wI') as out_pins:
        out_pins.write(1)     # Set p1_gpio_gen0 pin of group HIGH
        time.sleep(0.2)
        out_pins.write(2)     # Set p1_gpio_gen1 pin of group HIGH
        time.sleep(0.2)
        out_pins.write(0)     # Set both pin group GPIO pins LOW
        time.sleep(0.2)

def toggle_gpio_gen0_gen1_sequence():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()
                                 , pingroup.PinId.p1_gpio_gen1()
                                 ]
                               , 'wS') as out_pins:
        out_pins.write([True,True])   # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write([False,False]) # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write([1,1])         # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write([0,0])         # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write([23,42])       # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write([None,None])   # Set both pin group GPIO pins LOW
        time.sleep(0.2)
        out_pins.write(['1','1'])     # Set both pin group GPIO pins HIGH
        time.sleep(0.2)
        out_pins.write(['0','0'])     # Set both pin group GPIO pins LOW
        time.sleep(0.2)

def cycle_gpio_gen0_gen1_sequence():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()
                                 , pingroup.PinId.p1_gpio_gen1()
                                 ]
                               , 'wS') as out_pins:
        out_pins.write([True,False])  # Set p1_gpio_gen0 pin of group HIGH
        time.sleep(0.2)
        out_pins.write([False,True])  # Set p1_gpio_gen1 pin of group HIGH
        time.sleep(0.2)
        out_pins.write([False,False]) # Set both pin group GPIO pins LOW
        time.sleep(0.2)

if __name__ == '__main__':
    try:
        toggle_gpio_gen0_gen1_integer()
        time.sleep(0.8)
        toggle_gpio_gen0_gen1_sequence()
        time.sleep(0.8)
        cycle_gpio_gen0_gen1_integer()
        time.sleep(0.8)
        cycle_gpio_gen0_gen1_sequence()
    except error.GPIOError, e:
        print "Oops unexpected GPIO related error:",\
                e.__class__.__name__,':', e
    except ValueError:
        print "Oops unexpected value error!"
