'''
    Part of the dibase.rpi.gpio package.

    Exception classes for gpio package specific errors

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

class GPIOError(Exception):
    """A general GPIO operation exception occured"""
    pass

class PinIdInvalidError(GPIOError):
    """Using a GPIO pin id value that is invalid for this system"""
    pass

class PinInUseError(GPIOError):
    """The requested GPIO pin is currently in use"""
    pass

class PinOpenModeInvalidError(GPIOError):
    """
        The requested open mode string is invalid.
        Should be 'r' or 'w' optionally followed by 'N', 'R', 'F' or 'B'.
        Missing or empty defaults to 'rN'; no second letter implies 'N'.
        'R', 'F' and 'B' only valid for readers ('r' first mode letter).
    """
    pass

class PinBlockModeInvalidError(PinOpenModeInvalidError):
    """ 
        The requested wait mode character is invalid.
        Should be 'R', 'F' or 'B', or 'N' for no wait mode.
    """
    pass

class PinDirectionModeInvalidError(PinOpenModeInvalidError):
    """
        The requested read-write mode character is invalid.
        Should be 'r' or 'w'
    """
    pass
