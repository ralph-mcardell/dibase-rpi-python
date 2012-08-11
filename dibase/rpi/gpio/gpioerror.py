'''
    Part of the dibase.rpi.gpio package.

    Exception classes for gpio package specific errors

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

class GPIOError(Exception):
    """A general GPIO operation error occured"""
    def __init__(self):
        super(GPIOError, self).__init__(self.__doc__)

class PinIdInvalidError(GPIOError):
    """Invalid GPIO pin id value for this system"""
    pass

class PinInUseError(GPIOError):
    """Attempt to use a GPIO pin that is exported and maybe in use"""
    pass

class PinOpenModeInvalidError(GPIOError):
    """Invalid open mode, expected 'wN', 'rN', 'rR', 'rF' or 'rB'"""
    pass

class PinBlockModeInvalidError(PinOpenModeInvalidError):
    """Invalid blocking mode, expected 'R', 'F', 'B', or 'N'"""
    pass

class PinDirectionModeInvalidError(PinOpenModeInvalidError):
    """Invalid read-write mode, expected 'r' or 'w'"""
    pass
