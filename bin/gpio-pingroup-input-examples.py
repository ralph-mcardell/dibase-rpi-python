#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of using multiple pin IO objects to input from GPIO pins.

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

def poll_GPIO_GEN6_GCLK_opened_non_blocking_integer():
    INTERVAL = 1.0 # seconds
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rNI' ) as in_pins:
        print "Start sampling GPIO_GEN6 and GPIO_GCLK (open mode rNI) ..."
        time.sleep(INTERVAL)
        first_sample = in_pins.read()
        time.sleep(INTERVAL)
        second_sample = in_pins.read()
        time.sleep(INTERVAL)
        third_sample = in_pins.read()
        print "Read 3 samples from P1 GPIO_GEN6, GPIO_GCLK at approximately",\
               INTERVAL, "second intervals:", first_sample, second_sample,\
               third_sample

def poll_GPIO_GEN6_GCLK_opened_non_blocking_sequence():
    INTERVAL = 1.0 # seconds
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rNS' ) as in_pins:
        print "Start sampling GPIO_GEN6 and GPIO_GCLK (open mode rNS) ..."
        time.sleep(INTERVAL)
        first_sample = list(in_pins.read())
        time.sleep(INTERVAL)
        second_sample = list(in_pins.read())
        time.sleep(INTERVAL)
        third_sample = list(in_pins.read())
        print "Read 3 samples from P1 GPIO_GEN6, GPIO_GCLK at approximately",\
              INTERVAL, "second intervals:", first_sample, second_sample,\
              third_sample

def poll_GPIO_GEN6_GCLK_opened_blocking_on_rising_edge_integer():
    INTERVAL = 1.0 # seconds
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rRI' ) as in_pins:
        print "Start sampling GPIO_GEN6 and GPIO_GCLK (open mode rRI) ..."
        in_pins.read() # returns immediately with initial state of pins
        time.sleep(INTERVAL)
        first_sample = in_pins.read(0)
        time.sleep(INTERVAL)
        second_sample = in_pins.read(0)
        time.sleep(INTERVAL)
        third_sample = in_pins.read(0)
        print "Read 3 samples from P1 GPIO_GEN6, GPIO_GCLK at approximately",\
              INTERVAL, "second intervals:", first_sample, second_sample,\
              third_sample

def poll_GPIO_GEN6_GCLK_opened_blocking_on_rising_edge_sequence():
    INTERVAL = 1.0 # seconds
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rRS' ) as in_pins:
        print "Start sampling GPIO_GEN6 and GPIO_GCLK (open mode rRS) ..."
        in_pins.read() # returns immediately with initial state of pins
        time.sleep(INTERVAL)
        first_sample = list(in_pins.read(0))
        time.sleep(INTERVAL)
        second_sample = list(in_pins.read(0))
        time.sleep(INTERVAL)
        third_sample = list(in_pins.read(0))
        print "Read 3 samples from P1 GPIO_GEN6, GPIO_GCLK at approximately",\
              INTERVAL, "second intervals:", first_sample, second_sample,\
              third_sample

def wait_on_rising_edge_GPIO_GEN6_GCLK_no_timeout_integer():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rRI' ) as in_pins:
        in_pins.read() # returns immediately with initial state of pins
        print "Start sampling 3 transitions to HIGH state on P1 GPIO_GEN6 or GPIO_GCLK..."
        in_pins.read()
        print "High once"
        in_pins.read()
        print "High twice"
        in_pins.read()
        print "High thrice"
        print "P1 GPIO_GEN6 or GPIO_GCLK gone high 3 times"

def wait_on_rising_edge_GPIO_GEN6_GCLK_no_timeout_sequence():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rRS' ) as in_pins:
        in_pins.read() # returns immediately with initial state of pins
        print "Start sampling 3 transitions to HIGH state on P1 GPIO_GEN6 or GPIO_GCLK..."
        first_sample = list(in_pins.read())
        print "High once"
        second_sample = list(in_pins.read())
        print "High twice"
        third_sample = list(in_pins.read())
        print "High thrice"
        print "P1 GPIO_GEN6 or GPIO_GCLK gone high 3 times, returned values were",\
               first_sample, second_sample, third_sample

def wait_on_both_GPIO_GEN6_GCLK_no_timeout_integer():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rBI' ) as in_pins:
        in_pins.read()   # returns immediately with initial state of pins
        print "Start waiting for 3 state changes on P1 GPIO_GEN6 or GPIO_GCLK..."
        first_sample = in_pins.read()
        second_sample = in_pins.read()
        third_sample = in_pins.read()
        print "Read 3 samples from P1 GPIO_GEN6 and GPIO_GCLK ",\
               first_sample, second_sample, third_sample

def wait_on_both_GPIO_GEN6_GCLK_no_timeout_sequence():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rBS' ) as in_pins:
        in_pins.read()   # returns immediately with initial state of pins
        print "Start waiting for 3 state changes on P1 GPIO_GEN6 or GPIO_GCLK..."
        first_sample = list(in_pins.read())
        second_sample = list(in_pins.read())
        third_sample = list(in_pins.read())
        print "Read 3 samples from P1 GPIO_GEN6 and GPIO_GCLK ",\
               first_sample, second_sample, third_sample

def wait_on_both_GPIO_GEN6_GCLK_with_timeouts_integer():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rBI' ) as in_pins:
        in_pins.read()   # returns immediately with initial state of pins

        print "Waiting for 0.0001s for state change on P1 GPIO_GEN6 or GPIO_GCLK, timeout probable..."
        value = in_pins.read( 0.0001 )

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

        print "Waiting for 10000s for state change on P1 GPIO_GEN6 or GPIO_GCLK, timeout less probable..."
        value = in_pins.read( 10000 )

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

def wait_on_both_GPIO_GEN6_GCLK_with_timeouts_sequence():
    with pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()
                                 , pingroup.PinId.p1_gpio_gclk()
                                 ], 'rBS' ) as in_pins:
        in_pins.read()   # returns immediately with initial state of pins

        print "Waiting for 0.0001s for state change on P1 GPIO_GEN6 or GPIO_GCLK, timeout probable..."
        value = in_pins.read(0.0001)

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

        print "Waiting for 10000s for state change on P1 GPIO_GEN6 or GPIO_GCLK, timeout less probable..."
        value = in_pins.read(10000)

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

if __name__ == '__main__':
    try:
        INTERVAL = 0.3 # seconds
        poll_GPIO_GEN6_GCLK_opened_non_blocking_integer()
        time.sleep( INTERVAL )
        poll_GPIO_GEN6_GCLK_opened_non_blocking_sequence()
        time.sleep( INTERVAL )
        poll_GPIO_GEN6_GCLK_opened_blocking_on_rising_edge_integer()
        time.sleep( INTERVAL )
        poll_GPIO_GEN6_GCLK_opened_blocking_on_rising_edge_sequence()
        time.sleep( INTERVAL )
        wait_on_rising_edge_GPIO_GEN6_GCLK_no_timeout_integer()
        time.sleep( INTERVAL )
        wait_on_rising_edge_GPIO_GEN6_GCLK_no_timeout_sequence()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GEN6_GCLK_no_timeout_integer()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GEN6_GCLK_no_timeout_sequence()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GEN6_GCLK_with_timeouts_integer()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GEN6_GCLK_with_timeouts_sequence()
    except error.GPIOError, e:
        print "Oops unexpected GPIO related error:",\
                e.__class__.__name__,':', e
    except ValueError:
       print "Oops unexpected value error!"
