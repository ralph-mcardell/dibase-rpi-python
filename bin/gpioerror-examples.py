#!/usr/bin/python
'''
    Example uses of the dibase.rpi.gpio package modules.

    Shows examples of raising and handling gpioerror exceptions.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import sys
if __name__ == '__main__':
    sys.path.insert(0, './..')
import dibase.rpi.gpio.gpioerror as error

def raise_gpioerror():
    try:
        raise error.GPIOError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

def raise_pinidinvaliderror():
    try:
        raise error.PinIdInvalidError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

def raise_pininuseerror():
    try:
        raise error.PinInUseError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

def raise_pinopenmodeinvaliderror():
    try:
        raise error.PinOpenModeInvalidError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

def raise_pinblockmodeinvaliderror():
    try:
        raise error.PinBlockModeInvalidError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

def raise_pindirectionmodeinvaliderror():
    try:
        raise error.PinDirectionModeInvalidError
    except error.GPIOError,e:
        print e.__class__.__name__,':', e

if __name__ == '__main__':
    print "------------------------------------------------------------------"
    raise_gpioerror()
    print "------------------------------------------------------------------"
    raise_pinidinvaliderror()
    print "------------------------------------------------------------------"
    raise_pininuseerror()
    print "------------------------------------------------------------------"
    raise_pinopenmodeinvaliderror()
    print "------------------------------------------------------------------"
    raise_pinblockmodeinvaliderror()
    print "------------------------------------------------------------------"
    raise_pindirectionmodeinvaliderror()
    print "------------------------------------------------------------------"

