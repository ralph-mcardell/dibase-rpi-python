'''
    Part of the dibase.rpi.gpio package.

    Definitions and support for creating various Linux sys filsystem paths
    for GPIO operations.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

def gpio_path():
    ''' Return base path for GPIO 'files' and 'directories' '''
    return '/sys/class/gpio'

def export_file():
    ''' Returns the filename to write to to export a GPIO pin '''
    return 'export'

def unexport_file():
    ''' Returns the filename to write to to unexport a GPIO pin '''
    return 'unexport'

def pin_dir_base():
    ''' Returns the directory base name for exported GPIO pin 'files' '''
    return 'gpio'

def pin_direction_file():
    ''' Returns the pin data direction control 'file' name '''
    return 'direction'

def pin_value_file():
    ''' Returns the pin data value 'file' name '''
    return 'value'

def pin_edgemode_file():
    ''' Returns the pin edge detection notification mode 'file' name '''
    return 'edge'

def export_path():
    ''' Returns the path to GPIO pin export requests 'file' '''
    return ''.join( [gpio_path(), '/', export_file()] )

def unexport_path():
    ''' Returns the path to GPIO pin unexport requests 'file' '''
    return ''.join( [gpio_path(), '/', unexport_file()] )

def pin_path(pin_id):
    '''
        Returns the path to a specifically exported GPIO pin 'directory'
    
        pin_id should be a positive integer value that should have been
        validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
        possibly the subset available on the Raspberry Pi P1 connector.
        Note that no validation is done by pin_Path.
    '''
    return ''.join([gpio_path(), '/'\
                  , pin_dir_base(), str(pin_id)]\
                  )

def direction_path(pin_id):
    '''
        Returns the path to a exported GPIO pin's data direction 'file'
    
        pin_id should be a positive integer value that should have been
        validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
        possibly the subset available on the Raspberry Pi P1 connector.
        Note that no validation is done by direction_Path.
    '''
    return ''.join([pin_path(pin_id), '/'\
                  , pin_direction_file()]\
                  )

def edgemode_path(pin_id):
    '''
        Returns the path to a exported GPIO pin's data edge mode 'file'
    
        pin_id should be a positive integer value that should have been
        validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
        possibly the subset available on the Raspberry Pi P1 connector.
        Note that no validation is done by edgemode_Path.
    '''
    return ''.join([pin_path(pin_id), '/'\
                  , pin_edgemode_file()]\
                  )

def value_path(pin_id):
    '''
        Returns the path to a exported GPIO pin's data value 'file'
    
        pin_id should be a positive integer value that should have been
        validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
        possibly the subset available on the Raspberry Pi P1 connector.
        Note that no validation is done by value_Path.
    '''
    return ''.join( [pin_path(pin_id), '/', pin_value_file()] )
