'''
    Part of the dibase.rpi.gpio package.

    Abstract base classes defining IO operations for GPIO pins

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import abc    # for abstract base classes

class GPIOBase(object):
    '''
        Fully abstract base class interface as base for all GPIO IO classes.
        Similar to io.IOBase, except that actual IO functions are split off
        into abstract base sub-classes.
        This can be done as the BCM2835/BCM2807 GPIO pins are either in input
        mode (i.e. read) OR output mode (i.e. write) but not both at the same
        time.
        Defines common operations for GPIO pins that make sense: close, closed,
        fileno, readable, writable in the style of io.IOBase. Also included is
        the GPIO specific query method blocking.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def close( self ):
        ''' Close open GPIO resource (e.g. an output pin) '''
        pass

    @abc.abstractmethod
    def closed( self ):
        ''' Returns a True/False indicating whether an instance is closed '''
        pass

    @abc.abstractmethod
    def fileno( self ):
        '''
            Returns underlying integer file descriptor number (if any)
            associated with resource.
        '''
        pass

    @abc.abstractmethod
    def readable( self ):
        ''' Returns a True if resource can be read (input) '''
        pass

    @abc.abstractmethod
    def writable( self ):
        ''' Returns a True if resource can be written (output) '''
        pass

    @abc.abstractmethod
    def blocking( self ):
        ''' 
            Returns a True if IO blocks, False if it does not.
        '''
        pass

class GPIOReaderBase(GPIOBase):
    '''
        Abstract base class for classes supporting GPIO pin reading (input)
        This class assumes concrete type instances are readable, not writable
        AND not blocking (see GPIOWaitableReaderBase).
    '''
    __metaclass__ = abc.ABCMeta

    def readable( self ):
        ''' Returns True: readers are readable! '''
        return True

    def writable( self ):
        ''' Returns False: not a reader-writer '''
        return False

    def blocking( self ):
        ''' 
            Returns False - use GPIOWaitableReaderBase for 
            blocking readers
        '''
        return False

    @abc.abstractmethod
    def read( self ):
        '''
            Returns integer - each bit reflects momentary state of
            GPIO bits managed by reasource
        '''
        pass

class GPIOWriterBase(GPIOBase):
    '''
        Abstract base class for classes supporting GPIO pin writing (output)
        This class assumes concrete type instances are writable, not readable
        and not blocking as it makes no sense to wait on output transitions
        this way.
    '''
    __metaclass__ = abc.ABCMeta

    def readable( self ):
        ''' Returns False: not a reader-writer '''
        return False

    def writable( self ):
        ''' Returns True: writers are writable! '''
        return True

    def blocking( self ):
        ''' Returns a False - output does not block. '''
        return False

    @abc.abstractmethod
    def write( self, value ):
        '''
            Outputs integer - each bit reflects updated (latched) state
            of GPIO bits managed by reasource
        '''
        pass

class GPIOWaitableReaderBase(GPIOReaderBase):
    '''
        Abstract base class for classes supporting GPIO pin reading (input)
        with edge event notifications (value state transitions) enabled
        allowing waiting for such events to occur.
        This class assumes concrete type instances are readable, not writable
        AND ARE blocking.
    '''
    __metaclass__ = abc.ABCMeta

    def readable( self ):
        ''' Returns True: readers are readable! '''
        return True

    def writable( self ):
        ''' Returns False: not a reader-writer '''
        return False

    def blocking( self ):
        ''' Returns True - this is a blocking type. '''
        return True

    @abc.abstractmethod
    def wait( self, timeout=False ):
        '''
            Returns when one or more input GPIO lines managed by
            the resource changes state in a way that is monitored
            or after the timeout time, if specified, has elapsed.
        '''
        pass

    @abc.abstractmethod
    def reset( self ):
        ''' Resets previously signalled events causing wait to return '''
        pass
