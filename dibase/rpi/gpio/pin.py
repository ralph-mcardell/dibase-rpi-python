'''
    Part of the dibase.rpi.gpio package.

    Operations on single GPIO pins.
    Uses userspace sys filesystem GPIO interface.
    Provides a pin type and operations on instances modelled after file objects.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import os
import select # select.select used to wait on i/ps with edge interrupts enabled

from gpioerror import PinInUseError
from gpioerror import PinOpenModeInvalidError
from gpioerror import PinWaitModeInvalidError
from gpioerror import PinDirectionModeInvalidError
from pinid import PinId
from sysfspaths import Paths
from gpiobase import GPIOReaderBase
from gpiobase import GPIOWriterBase
from gpiobase import GPIOWaitableReaderBase

def force_free_pin( pin_id ):
    '''
        Will 'free' a pin by unexporting it from the sys filesystem if it
        is exported. Intended to be used in cases where some failure has
        left pins exported which should not have been. It is considered
        preferable to have GPIO pin IO classes back off if a pin they are
        asked to use is already exported so as not to trample on other
        users' toes as it were. However this leaves the possibility that
        pins are accidentally left exported due to bad process termination.

        pin_id is the raw GPIO pin id to free.

        Returns None if the pin was not exported or the pin_id value if it
        was and had to be unexported.
        
        Throws a pin.PinIdInvalidError if the pin_id is invalid
    '''
    unexported = None
    if os.path.exists(Paths.pin_path( pin_id )):
        unexported = pin_id
        with open(Paths.unexport_path(), 'w') as unexport_file:
            unexport_file.write( str(pin_id) )
    return unexported

class WaitMode(object):
    '''
        Class encapsulating open wait mode characters and their equivalent
        sys filesystem GPIO edge mode file values.
    '''
    @classmethod
    def not_waitable_open_mode( cls ):
        ''' Return character for open wait mode no-waiting mode '''
        return 'N'

    @classmethod
    def not_waitable_edge_mode( cls ):
        ''' Return string for edge file wait no-waiting mode '''
        return 'none'

    @classmethod
    def wait_on_rising_edge_open_mode( cls ):
        ''' Return character for open wait on rising edge mode '''
        return 'R'

    @classmethod
    def wait_on_rising_edge_edge_mode( cls ):
        ''' Return string for edge file rising edge mode '''
        return 'rising'

    @classmethod
    def wait_on_falling_edge_open_mode( cls ):
        ''' Return character for open wait on falling edge mode '''
        return 'F'

    @classmethod
    def wait_on_falling_edge_edge_mode( cls ):
        ''' Return string for edge file falling edge mode '''
        return 'falling'

    @classmethod
    def wait_on_both_edges_open_mode( cls ):
        ''' Return character for open wait on both edges mode '''
        return 'B'

    @classmethod
    def wait_on_both_edges_edge_mode( cls ):
        ''' Return string for edge file both edges mode '''
        return 'both'
    
    @classmethod
    def all_wait_open_mode_characters( cls ):
        ''' Return string of all open wait mode characters '''
        return ''.join([ WaitMode.not_waitable_open_mode()
                       , WaitMode.wait_on_rising_edge_open_mode()
                       , WaitMode.wait_on_falling_edge_open_mode()
                       , WaitMode.wait_on_both_edges_open_mode()
                       ])

    @classmethod
    def is_valid_wait_open_mode( cls, mode ):
        ''' 
            Return True if passed mode value is a valid single open wait
            mode character.
        '''
        return len(mode)==1 and \
                (mode in WaitMode.all_wait_open_mode_characters())

    def __init__(self, wait_mode):
        '''
            Creates a WaitMode instance from an open wait mode character.
            Raises a PinWaitModeInvalidError exception if wait_mode
            is not a valid open wait mode character.
        '''
        if not WaitMode.is_valid_wait_open_mode(wait_mode):
            raise PinWaitModeInvalidError
        self.__value = wait_mode

    def is_waitable(self):
        '''
            Returns True if WaitMode instance represents a mode which will
            wait for an event. That is for any mode except not waitable.
        '''
        return self.__value != WaitMode.not_waitable_open_mode()

    def open_mode_value(self):
        '''
            Returns the character value of the open wait mode the WaitMode
            instance represents which will be the wait_mode value used to 
            create the instance.
        '''
        return self.__value

    def edge_mode_value(self):
        '''
            Returns the string value for the sys filesystem GPIO edge file
            for the edge mode the WaitMode instance represents.
        '''
        if self.__value == WaitMode.wait_on_rising_edge_open_mode():
            return WaitMode.wait_on_rising_edge_edge_mode()
        elif self.__value == WaitMode.wait_on_falling_edge_open_mode():
            return WaitMode.wait_on_falling_edge_edge_mode()
        elif self.__value == WaitMode.wait_on_both_edges_open_mode():
            return WaitMode.wait_on_both_edges_edge_mode()
        elif self.__value == WaitMode.not_waitable_open_mode():
            return WaitMode.not_waitable_edge_mode()
        else:
            raise PinWaitModeInvalidError

class DirectionMode(object):
    '''
        Class encapsulating open IO direction mode characters and their
        equivalent sys filesystem GPIO direction file values.
    '''
    @classmethod
    def read_open_mode( cls ):
        ''' Return character for open read mode '''
        return 'r'

    @classmethod
    def read_direction_mode( cls ):
        ''' Return string for direction file input (read) mode '''
        return 'in'

    @classmethod
    def write_open_mode( cls ):
        ''' Return character for open write mode '''
        return 'w'

    @classmethod
    def write_direction_mode( cls ):
        ''' Return string for direction file output (write) mode '''
        return 'out'

    @classmethod
    def all_direction_open_mode_characters( cls ):
        ''' Return string of all open direction mode characters '''
        return ''.join([ DirectionMode.read_open_mode()
                       , DirectionMode.write_open_mode()
                       ])

    @classmethod
    def is_valid_direction_open_mode( cls, mode ):
        ''' 
            Return True if passed mode value is a valid single open direction
            mode character.
        '''
        return len(mode)==1 and \
                (mode in DirectionMode.all_direction_open_mode_characters())

    def __init__(self, direction_mode):
        '''
            Creates a DirectionMode instance from an open direction mode
            character. Raises a PinDirectionModeInvalidError exception if
            direction_mode is not a valid open direction mode character.
        '''
        if not (DirectionMode.is_valid_direction_open_mode(direction_mode)):
            raise PinDirectionModeInvalidError
        self.__value = direction_mode

    def is_read(self):
        ''' Returns True if DirectionMode instance is read/input mode. '''
        return self.__value == DirectionMode.read_open_mode()

    def is_write(self):
        ''' Returns True if DirectionMode instance is write/output mode. '''
        return self.__value == DirectionMode.write_open_mode()

    def open_mode_value(self):
        '''
            Returns the character value of the open direction mode the
            DirectionMode instance represents which will be the
            direction_mode value used to create the instance.
        '''
        return self.__value

    def direction_mode_value(self):
        '''
            Returns the string value for the sys filesystem GPIO direction
            file for the direction mode the DirectionMode instance represents.
        '''
        if self.__value == DirectionMode.read_open_mode():
            return DirectionMode.read_direction_mode()
        elif self.__value == DirectionMode.write_open_mode():
            return DirectionMode.write_direction_mode()
        else:
            raise PinDirectionModeInvalidError

class _PinIOBase(object):
    '''
        Internal mixin base class for concrete Pin IO classes.
        Provides common functionality.
    '''
    def __init__(self, pin_id, direction_mode, wait_mode):
        '''
            Provide common initialisation for GPIO pin IO.
            Parameterised on pin id, and direction and wait modes
            - Ensures pin_id is a PinId value. Raises PinIdInvalidError
              if it is not a valid PinId value
            - Ensures direction_mode is a DirectionMode value. Raises
              PinDirectionModeInvalidError if it is not a valid DirectionMode
              value
            - Ensures wait_mode is a WaitMode value. Raises
              PinWaitModeInvalidError if it is not a valid WaitMode value
            - Calls _validate_init_parameters to perform customisable
              validation. Base implementation raises a PinInUseError if
              the pin is already exported in the sys filesystem
            - Exports the pin in the sys filesystem
            - Sets the direction of data in line with direction_mode
            - Sets the edge file's change event notification mode value
              to reflect the wait_mode.
            - Opens the sys filesystem GPIO pin's value file for reading
              or writing in accordance with direction_mode and holds it open
        '''
        self.__value_file = None # *must* have __value_file attribute
        # Ensure we have a good pin_id value
        if not isinstance(pin_id, PinId):
            pin_id = PinId.gpio(pin_id)
        self.__pin_id = pin_id
        if not isinstance(direction_mode, DirectionMode):
            direction_mode = DirectionMode(direction_mode)
        if not isinstance(wait_mode, WaitMode):
            wait_mode = WaitMode(wait_mode)

        self.cb_validate_init_parameters(pin_id, direction_mode, wait_mode)

        # export
        with open(Paths.export_path(), 'w') as export_file:
            export_file.write( str(pin_id) )

        # set edge mode file's value
        with open(Paths.edgemode_path(pin_id), 'w') as edge_file:
            edge_file.write( wait_mode.edge_mode_value() )

        # set i/o direction
        with open(Paths.direction_path(pin_id), 'w') as direction_file:
            direction_file.write(direction_mode.direction_mode_value())

        # open value 'file' for reading/writing depending on direction mode
        self.__value_file = open( Paths.value_path(pin_id)\
                                        , direction_mode.open_mode_value()+'b'
                                        )

    def __del__(self):
        ''' Calls close to try to ensure pin is cleanly freed up '''
        self.close()

    def __enter__(self):
        ''' Just returns self as object for use 'as' in 'with' statement '''
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        ''' Ensures close called on exit from 'with' statement '''
        self.close()

    def cb_validate_init_parameters(self, pin_id, direction_mode, wait_mode):
        '''
            Check parameters are valid. Raise exception if they are not.
            Base implementation checks pin_id is not already exported.
            Sub-classes should override, add additional checks and call
            this super class implementation. Note that basic parameter
            checks are performed before _validate_init_parameters is called
            by converting parameters to instances of their specific,
            validated, handling types: PinId, DirectionMode and WaitMode.
        '''
        # Raise a PinInUseError if pin is currently exported
        if os.path.exists(Paths.pin_path(pin_id)):
            raise PinInUseError

    def closed(self): 
        ''' Returns True if the Pin has been closed, False if it is open '''
        return self.__value_file == None

    def close( self ):
        '''
            Closes the pin. Can be called repeatedly safely on the same
            object. Closes pin's sys filesystem value file and unexports
            the pin from the sys filesystem.
        '''
        if ( not self.closed() ):
            self.__value_file.close()
            self.__value_file = None
            # Unexport if exported (should be unless somone sneaking around
            # behind our backs!)
            if os.path.exists(Paths.pin_path( self.__pin_id )):
                with open(Paths.unexport_path(), 'w') as unexport_file:
                    unexport_file.write( str(self.__pin_id) )
            self.__pin_id = None

    def fileno(self):
        '''
            If the Pin IO object is open return the underlying file
            descriptor number of the pin's sys filesystem value file. If the
            object is closed then returns None.
        '''
        if (not self.closed() ):
            return self.__value_file.fileno()
        else:
            return None

    def _value_file(self):
        '''
            Internal use function returns the __value_file file attribute
            so that sub classes can operate on it.
        '''
        return self.__value_file

class PinWriter(_PinIOBase, GPIOWriterBase):
    '''
        Concrete GPIOWriterBase implementation for a single GPIO pin.
        It can handle writing single 0 or 1 values to the related GPIO
        pin, which will have been exported and set up for output as part
        of the initialisation.
    '''
    def __init__(self, pin_id):
        '''
            Initialise a PinWriter instance for writing with no waiting.
        '''
        super(PinWriter, self).__init__(pin_id, 'w','N')

    def write(self, value):
        '''
            Output a 1 or 0 to an open pin GPIO line. Raises a ValueError
            if the object is closed.

            value is a value that can be interpreted as True (1 output) or
            False (0 output). A special case is that '0', normally considered
            True, is considered a False value and therefore causes a 0 output.
         '''
        if self.closed():
            raise ValueError
        value = 0 if value == '0' else value
        self._value_file().seek(0)
        self._value_file().write('1' if value else '0')

class PinReader(_PinIOBase, GPIOReaderBase):
    '''
        Concrete GPIOReaderBase implementation for a single GPIO pin.
        Handles reading single 0 or 1 values from the related GPIO pin,
        which will have been exported and set up for input as part of the
        initialisation. Note that the read operation does not wait for a
        state change of the pin - it returns the current pin value 'now'
        and so is only blocking in terms of IO operation timing.
    '''

    def __init__(self, pin_id):
        ''' Initialise a PinReader instance for reading and no waiting. '''
        super(PinReader, self).__init__(pin_id, 'r','N')

    def read(self):
        '''
            Returns a True if 1 read from an open pin GPIO line, else False.
            Raises a ValueError if the object is closed.
       '''
        if self.closed():
            raise ValueError

        # reset any previously latched input value and rewind to file start
        self._value_file().read()
        self._value_file().seek(0)

        return self._value_file().read(1) == '1'

class PinWaitableReader(_PinIOBase, GPIOWaitableReaderBase):
    '''
        Concrete GPIOWaitableReaderBase implementation for a single GPIO pin.
        Handles reading single 0 or 1 values from the related GPIO pin, which
        will have been exported and set up for input as part of the
        initialisation. Note that the read operation does not wait for a state
        change of the pin - it returns the current pin value 'now' and so is
        only blocking in terms of IO operation timing. To wait, call wait,
        which will return on one of the requested pin state changes 
        ('R':rising edge 0->1 transition, 'F':falling edge 1->0
        transition, or 'B':both).
    '''

    def __init__(self, pin_id, wait_mode):
        '''
            Initialise a PinWaitableReader instance for reading with the requested
            waitable wait mode.
        '''
        super(PinWaitableReader, self).__init__(pin_id, 'r', wait_mode)

    def cb_validate_init_parameters(self, pin_id, direction_mode, wait_mode):
        if ( not wait_mode.is_waitable() ):
            raise PinWaitModeInvalidError
        super(PinWaitableReader, self).\
            cb_validate_init_parameters(pin_id, direction_mode, wait_mode)

    def read(self):
        '''
            Returns a True if 1 read from an open pin GPIO line, else False.
            Raises a ValueError if the object is closed.
       '''
        if self.closed():
            raise ValueError
        self._value_file().seek(0)
        return self._value_file().read(1) == '1'

    def wait( self, timeout=False ):
        '''
            Returns when the pin signals a waited for value 'edge' transition
            occurs or after the timeout time, in seconds, if specified, has
            elapsed. No timeout value  will cause a wait 'forever' or until a
            monitored event occurs. A zero timeout will return immediately.
            
            Raises a ValueError if the instance is closed.

            Returns self, as only possible notified entity or None if
            timeout expired before any notification events were received.
            
        '''
        if self.closed():
            raise ValueError

        if timeout:
            changed = select.select( [], [], [self], timeout )
            if changed == ([], [], []): # Triple of empty lists=>call timed-out
                return None
            else:
                self.read()  # grab value: will latch until reset
                return self
        else:
            changed = select.select( [], [], [self] )
            self.read()  # grab value: will latch until reset
            return self

    def reset( self ):
        '''
            Resets previously signalled events causing wait to return
            Raises a ValueError if instance is closed
        '''
        if self.closed():
            raise ValueError
        # Reading all from value file clears edge event notification
        self._value_file().read()

def open_pin( pin_id, mode='' ):
    '''
        Factory function creating GPIO pin objects of appropriate types for
        the requested operational mode.

        pin_id is a BCM2835 (or BCM2807) GPIO id number, probably one
        connected to the Raspberry Pi P1 connector. It can be a PinId type or
        an int (which will be validated).

        mode is optional. 
        If passed it should be a string of 0, 1, or 2 characters.
        The first character of the mode string indicates the desired data
        direction: read/input: 'r' or write/output: 'w'
        The second, optional, character indicates the wait mode:
        wait on nothing: 'N', 
        wait on rising edge events (0 to 1 transitions): 'R',
        wait on falling edge events (1 to 0 transitions): 'F',
        wait on events for both edges: 'B'.
        The default is 'N' wait on no events and is the only valid option when
        opening a pin for writing/output.
        No mode argument or an empty mode string defaults to read/input and
        not waiting for any edge events.

        Returns an object that implements one of the sub-types of GPIOBase:
            If write requested then returned object implements GPIOWriterBase
            If read requested then object returned implements GPIOReaderBase
                If wait on edge events mode other than 'N' requested then
                    returned object implements GPIOWaitableReaderBase.

        Will raise exception on error, which include specific GPIOError
        types:
            PinIdInvalidError if pin_id is invalid
            PinOpenModeInvalidError if mode is invalid:
                PinDirectionModeInvalidError if an invalid data direction mode
                character was specified
                PinWaitModeInvalidError if an invalid wait for edge events
                mode was specified for the specified data direction mode 
            PinInUseError if the requested pin_id to use was already
            exported (indicting some other process may be using it).
        In addition general Python exceptions such as IOError may be raised.
    '''
    mode_len = len(mode)
    direction_mode = DirectionMode(DirectionMode.read_open_mode())
    edge_mode = WaitMode(WaitMode.not_waitable_open_mode())
    if mode_len >= 1:
        direction_mode = DirectionMode( mode[0] )
        if mode_len == 2:
            edge_mode = WaitMode( mode[1] )
        elif mode_len > 2:
            raise PinOpenModeInvalidError
    if direction_mode.is_write():
        if edge_mode.is_waitable(): # any other wait mode meaningless for output
            raise PinWaitModeInvalidError
        return PinWriter( pin_id )
    else: # direction mode only read or write...
        assert( direction_mode.is_read() )
        if edge_mode.is_waitable():
            return PinWaitableReader( pin_id, edge_mode.open_mode_value() )
        else:
            return PinReader( pin_id )

#
