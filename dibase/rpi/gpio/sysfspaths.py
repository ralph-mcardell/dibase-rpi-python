'''
    Part of the dibase.rpi.gpio package.

    Definitions and support for creating various Linux sys filsystem paths
    for GPIO operations.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

class Paths(object):
    '''
        Utility class to manage Linux gpiolib sys filesystem userspace GPIO
        path name strings.

        Paths contains only class methods returning the various useful sysfs
        GPIO pin 'files' and 'directories'.
    '''
    @classmethod
    def gpio_path(cls):
        ''' Return base path for GPIO 'files' and 'directories' '''
        return '/sys/class/gpio'

    @classmethod
    def export_file( cls ):
        ''' Returns the filename to write to to export a GPIO pin '''
        return 'export'

    @classmethod
    def unexport_file( cls ):
        ''' Returns the filename to write to to unexport a GPIO pin '''
        return 'unexport'

    @classmethod
    def pin_dir_base( cls ):
        ''' Returns the directory base name for exported GPIO pin 'files' '''
        return 'gpio'

    @classmethod
    def pin_direction_file( cls ):
        ''' Returns the pin data direction control 'file' name '''
        return 'direction'

    @classmethod
    def pin_value_file( cls ):
        ''' Returns the pin data value 'file' name '''
        return 'value'

    @classmethod
    def pin_edgemode_file( cls ):
        ''' Returns the pin edge detection notification mode 'file' name '''
        return 'edge'

    @classmethod
    def export_path( cls ):
        ''' Returns the path to GPIO pin export requests 'file' '''
        return ''.join( [Paths.gpio_path(), '/', Paths.export_file()] )

    @classmethod
    def unexport_path(cls):
        ''' Returns the path to GPIO pin unexport requests 'file' '''
        return ''.join( [Paths.gpio_path(), '/', Paths.unexport_file()] )

    @classmethod
    def pin_path( cls, pin_id ):
        '''
            Returns the path to a specifically exported GPIO pin 'directory'
        
            pin_id should be a positive integer value that should have been
            validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
            possibly the subset available on the Raspberry Pi P1 connector.
            Note that no validation is done by pin_Path.
        '''
        return ''.join([Paths.gpio_path(), '/'\
                      , Paths.pin_dir_base(), str(pin_id)]\
                      )

    @classmethod
    def direction_path( cls, pin_id ):
        '''
            Returns the path to a exported GPIO pin's data direction 'file'
        
            pin_id should be a positive integer value that should have been
            validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
            possibly the subset available on the Raspberry Pi P1 connector.
            Note that no validation is done by direction_Path.
        '''
        return ''.join([Paths.pin_path(pin_id), '/'\
                      , Paths.pin_direction_file()]\
                      )

    @classmethod
    def edgemode_path( cls, pin_id ):
        '''
            Returns the path to a exported GPIO pin's data edge mode 'file'
        
            pin_id should be a positive integer value that should have been
            validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
            possibly the subset available on the Raspberry Pi P1 connector.
            Note that no validation is done by edgemode_Path.
        '''
        return ''.join([Paths.pin_path(pin_id), '/'\
                      , Paths.pin_edgemode_file()]\
                      )

    @classmethod
    def value_path( cls, pin_id ):
        '''
            Returns the path to a exported GPIO pin's data value 'file'
        
            pin_id should be a positive integer value that should have been
            validated as being acceptable as a BCM2835/BCM2807 GPIO pin -
            possibly the subset available on the Raspberry Pi P1 connector.
            Note that no validation is done by value_Path.
        '''
        return ''.join( [Paths.pin_path(pin_id), '/', Paths.pin_value_file()] )
