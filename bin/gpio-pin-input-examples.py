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

def poll_GPIO_GCLK_opened_non_blocking():
    INTERVAL = 1.0 # seconds
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rN' ) as in_pin:
        print "Start sampling GPIO_GCLK (open mode rN) ..."
        time.sleep(INTERVAL)
        first_sample = in_pin.read()
        time.sleep(INTERVAL)
        second_sample = in_pin.read()
        time.sleep(INTERVAL)
        third_sample = in_pin.read()
        print "Read 3 samples from P1 GPIO_GCLK at approximately", INTERVAL,\
              "second intervals:", first_sample, second_sample, third_sample

def poll_GPIO_GCLK_opened_blocking_on_rising_edge():
    INTERVAL = 1.0 # seconds
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rR' ) as in_pin:
        print "Start sampling GPIO_GCLK (open mode rR) ..."
        in_pin.read() # returns immediately with initial pin state
        time.sleep(INTERVAL)
        first_sample = in_pin.read(0)
        time.sleep(INTERVAL)
        second_sample = in_pin.read(0)
        time.sleep(INTERVAL)
        third_sample = in_pin.read(0)
        print "Read 3 samples from P1 GPIO_GCLK at approximately", INTERVAL,\
              "second intervals:", first_sample, second_sample, third_sample

def wait_on_rising_edge_GPIO_GCLK_no_timeout():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rR' ) as in_pin:
        in_pin.read() # returns immediately with initial pin state
        print "Start sampling 3 transitions to HIGH state on P1 GPIO_GCLK..."
        in_pin.read()
        print "High once"
        in_pin.read()
        print "High twice"
        in_pin.read()
        print "High thrice"
        print "P1 GPIO_GCLK gone high 3 times"

def wait_on_both_GPIO_GCLK_no_timeout():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rB' ) as in_pin:
        in_pin.read()   # returns immediately with initial pin state
        print "Start waiting for 3 state changes on P1 GPIO_GCLK..."
        first_sample = in_pin.read()
        second_sample = in_pin.read()
        third_sample = in_pin.read()
        print "Read 3 samples from P1 GPIO_GCLK ",\
               first_sample, second_sample, third_sample

def wait_on_both_GPIO_GCLK_with_timeouts():
    with pin.open_pin( pin.PinId.p1_gpio_gclk(), 'rB' ) as in_pin:
        in_pin.read()   # returns immediately with initial pin state

        print "Waiting for 0.0001s for state change on P1 GPIO_GCLK, timeout probable..."
        value = in_pin.read( 0.0001 )

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

        print "Waiting for 1000s for state change on P1 GPIO_GCLK, timeout less probable..."
        value = in_pin.read( 10000 )

        if value==None:
            print "Wait for input change timed out..."
        else:
            print "Value read:", value

if __name__ == '__main__':
    try:
        INTERVAL = 0.3 # seconds
        poll_GPIO_GCLK_opened_non_blocking()
        time.sleep( INTERVAL )
        poll_GPIO_GCLK_opened_blocking_on_rising_edge()
        time.sleep( INTERVAL )
        wait_on_rising_edge_GPIO_GCLK_no_timeout()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GCLK_no_timeout()
        time.sleep( INTERVAL )
        wait_on_both_GPIO_GCLK_with_timeouts()
    except error.GPIOError:
        print "Oops unexpected GPIO related error!"
    except ValueError:
       print "Oops unexpected value error!"
    except Exception:
        print "Oops really unexpected error of unanticipated error type!"
