#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of using single pin IO objects to input from GPIO pins.

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

def poll_GPIO_GCLK_input():
    INTERVAL = 1.0 # seconds
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rN' ) as in_pin:
        print "Start sampling..."
        time.sleep(INTERVAL)
        first_sample = in_pin.read()
        time.sleep(INTERVAL)
        second_sample = in_pin.read()
        time.sleep(INTERVAL)
        third_sample = in_pin.read()
        print "Read 3 samples from P1 GPIO_GCLK at approximately", INTERVAL,\
              "second intervals:", first_sample, second_sample, third_sample

def wait_both_GPIO_GCLK_input_no_timeout():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rB' ) as in_pin:
        print "Start sampling 3 state changes on P1 GPIO_GCLK..."
        in_pin.wait()   # returns immediately with initial pin state
        first_sample = in_pin.read()
        in_pin.reset()
        in_pin.wait()
        second_sample = in_pin.read()
        in_pin.reset()
        in_pin.wait()
        third_sample = in_pin.read()
        in_pin.reset()
        print "Read 3 samples from P1 GPIO_GCLK ",\
               first_sample, second_sample, third_sample

def wait_both_GPIO_GCLK_input_with_timeouts():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rB' ) as in_pin:
        in_pin.wait()   # returns immediately with initial pin state
        first_sample = in_pin.read()
        in_pin.reset()

        # wait for short period of time so likely to time out...
        changed = in_pin.wait( 0.0001 )

        if changed==None:
            print "Wait for input change timed out..."
        else:
            print "Value now:", changed.read()

        # wait for long period of time so less likely to time out...
        changed = in_pin.wait( 10000 )

        if changed==None:
            print "Wait for input change timed out..."
        else:
            print "Value now:", changed.read()

def wait_rising_edge_GPIO_GCLK_input_no_timeout():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rR' ) as in_pin:
        print "Start sampling 3 transitions to HIGH state on P1 GPIO_GCLK..."
        in_pin.reset()
        in_pin.wait()
        print "High once"
        in_pin.reset()
        in_pin.wait()
        print "High twice"
        in_pin.reset()
        in_pin.wait()
        print "High thrice"
        print "P1 GPIO_GCLK gone high 3 times"

def wait_rising_edge_GPIO_GCLK_input_long_pause_read_multiple():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rR' ) as in_pin:
        print "Start sampling transition to HIGH state on P1 GPIO_GCLK..."
        in_pin.reset()
        in_pin.wait()
        print "P1 GPIO_GCLK pin transitioned to a HIGH state."
        time.sleep( 3 )
        if in_pin.read():
            print "Read as High"
        else:
            print "Oops! Read as LOW"

        for i in range(0,20):
            time.sleep(0.2)
            print in_pin.read()

if __name__ == '__main__':
    try:
        wait_rising_edge_GPIO_GCLK_input_long_pause_read_multiple()
        wait_rising_edge_GPIO_GCLK_input_no_timeout()
        poll_GPIO_GCLK_input()
        wait_both_GPIO_GCLK_input_no_timeout()
        wait_both_GPIO_GCLK_input_with_timeouts()
    except error.GPIOError:
        print "Oops unexpected GPIO related error!"
    except ValueError:
       print "Oops unexpected value error!"
    except Exception:
        print "Oops really unexpected error of unanticipated error type!"
