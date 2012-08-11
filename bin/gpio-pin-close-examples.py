#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of closing open pin IO objects returned from the
    pin.open_pin function.
    
    Also demonstrates the use of pin.force_free_pin to forably ensure a pin
    IO object is closed and determining if it had to be forably closed.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import sys
if __name__ == '__main__':
    sys.path.insert(0, './..')
import dibase.rpi.gpio.pin as pin
import dibase.rpi.gpio.gpioerror as error

def open_pin_explicit_close():
    gpio_gen0_out = pin.open_pin(pin.PinId.p1_gpio_gen0(), 'w')
    assert( not gpio_gen0_out.closed() )
    gpio_gen0_out.close()
    assert( gpio_gen0_out.closed() )

def open_pin_implicit_close( pinId ):
    pin_in = pin.open_pin(pinId)
    assert( not pin_in.closed() )

def with_open_pin_closed_in_with_clause_exit_cleanup():
    outside_value = None
    with pin.open_pin( pin.PinId.p1_gpio_gen1() ) as p:
        outside_value = p
        assert( not p.closed() )
        assert( not outside_value.closed() )
    assert( outside_value.closed() )

if __name__ == '__main__':
    try:
        open_pin_explicit_close()    
        with_open_pin_closed_in_with_clause_exit_cleanup()
        open_pin_implicit_close(pin.PinId.p1_gpio_gen1())
    # Check requested pin opened by open_pin_implicit_close is closed
    # by checking return value from pin.force_free_pin:
        freed_pin_id = pin.force_free_pin(pin.PinId.p1_gpio_gen1())
        assert( freed_pin_id==None )
    except error.GPIOError,e:
        print "Oops unexpected GPIO related error:\n   ",\
                e.__class__.__name__,':', e
    except ValueError:
        print "Oops unexpected value error!"
