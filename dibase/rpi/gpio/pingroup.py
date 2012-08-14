'''
    Part of the dibase.rpi.gpio package.

    Operations on groups of GPIO pins.
    Uses userspace sys filesystem GPIO interface.
    Provides a set of types and operations to more easily perform IO on
    groups of GPIO pins modelled after file objects.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import os
import select # select.select used to wait on i/ps with edge interrupts enabled
import collections

from pinid import PinId
from gpioerror import GPIOError
from gpioerror import PinBlockModeInvalidError
from gpioerror import PinDirectionModeInvalidError
from gpioerror import PinGroupOpenModeInvalidError
from gpioerror import PinGroupFormatModeInvalidError
from gpioerror import PinGroupIdsInvalidError
from gpiobase import GPIOReaderBase
from gpiobase import GPIOWriterBase
from gpiobase import GPIOBlockingReaderBase
from pin import open_pin
from pin import BlockMode
from pin import DirectionMode

class FormatMode(object):
    '''Class encapsulating open IO data format mode characters'''
    @classmethod
    def integer_open_mode(cls):
        '''Return character for open integer data format mode'''
        return 'I'

    @classmethod
    def sequence_open_mode(cls):
        '''Return character for open sequecne data format mode'''
        return 'S'

    @classmethod
    def all_format_open_mode_characters(cls):
        '''Return string of all open foramt mode characters'''
        return ''.join([ FormatMode.integer_open_mode()
                       , FormatMode.sequence_open_mode()
                       ])

    @classmethod
    def is_valid_format_open_mode( cls, mode ):
        ''' 
            Return True if passed mode value is a valid single open format
            mode character.
        '''
        return len(mode)==1 and \
                (mode in FormatMode.all_format_open_mode_characters())

    def __init__(self, format_mode):
        '''
            Creates a FormatMode instance from an open format mode
            character. Raises a PinGroupFormatModeInvalidError exception if
            format_mode is not a valid open format mode character.
        '''
        if not (FormatMode.is_valid_format_open_mode(format_mode)):
            raise PinGroupFormatModeInvalidError
        self.__value = format_mode

    def is_integer(self):
        '''Returns True if FormatMode instance is integer format mode.'''
        return self.__value == FormatMode.integer_open_mode()

    def is_sequence(self):
        '''Returns True if FormatMode instance is sequence format mode.'''
        return self.__value == FormatMode.sequence_open_mode()

    def open_mode_value(self):
        '''
            Returns the character value of the open format mode the
            FormatMode instance represents which will be the
            format_mode value used to create the instance.
        '''
        return self.__value

class _PinGroupIOBase(object):
    '''
        Internal mixin base class for concrete Pin group IO classes.
        Provides common functionality.
    '''
    def __init__(self, pin_ids, mode):
        '''
            Common initalisation for GPIO pin group IO classes.

            pin_ids should be an iterable sequence of pin id values of the
            pins to be in group. It should contain at least one value
            otherwise a gpioerror.PinGroupIdsInvalidError exception is
            raised.
            
            mode is the required open mode for each _single_ pin in the pin
            group and is provided by sub classes.
            
            Additionally any exception that might be raised by pin.open_pin
            may be raised (other than those relating to bad mode values
            unless such a bad mode is passed from sub classes).
            
            On successful return an open pin group object will be open.
        '''
        self._pins = []
        if not (pin_ids and isinstance(pin_ids, collections.Iterable)):
            raise PinGroupIdsInvalidError
        for id in pin_ids:
            try:
                p = open_pin(id, mode)
                self._pins.append(p)
            except GPIOError, e:
            # Close open pins ASAP - do not wait for __del__ to be called
                for p in self._pins:
                    p.close()
                self._pins = []
                raise e

    def __del__(self):
        '''Calls close to try to ensure pin group is cleanly freed up'''
        if self._pins:
            self.close()

    def __enter__(self):
        '''Returns value of self'''
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''Calls close to ensure pin group is cleanly freed up'''
        self.close()

    def close(self):
        '''If not already closed then closes all pins in the group'''
        if not self.closed():
            for p in self._pins:
                p.close()

    def closed(self):
        '''Returns True if the pin group is closed, False if it is open'''
        return self._pins[0].closed()

    def file_descriptors(self):
        '''
            If an instance is closed returns an empty list otherwise returns
            a list containing the file descriptor of the open value
            file of each pin of the group in the order of the pin ids passed
            to __init__.
        '''
        if self.closed():
            return []
        else:
            fds = []
            for p in self._pins:
                fds.append(p.fileno())
            return fds

class PinWordWriter(_PinGroupIOBase, GPIOWriterBase):
    '''
        Concrete GPIOWriterBase implementation for a group of GPIO pins.
        It handles writing 0 or 1 values to the related GPIO pins presented
        as bits in an integer. Each GPIO pin in the group will have been
        exported and set up for output as part of the initialisation.
    '''
    def __init__(self, pin_ids):
        '''
            Creates a group of GPIO pins for writing (output) with pin bit
            values expressed to write as bits in an integer with bit 0
            indicating the value for the first pin in the group, and bit 1
            the next and so on. Pins are ordered arounding to the position
            of their id in the pin_ids argument.

            pin_ids should be an iterable sequence of pin id values of the
            pins to be in group. It should contain at least one value
            otherwise a gpioerror.PinGroupIdsInvalidError exception is
            raised. Additionally any exception that might be raised by
            pin.open_pin may be raised other than those relating to bad mode
            values.
            
            On successful return an open pin group object will be open and
            ready to write to. Otherwise it will be closed.
        '''
        super(PinWordWriter, self).__init__(pin_ids, 'wN')
        self._cached_value = None
        self._pin_bit_range = range(len(self._pins))
        self._pin_max_value = 2**len(self._pins)-1

    def write(self, value):
        '''
            Writes the value to the pins in the group.

            The passed value should be a positive integer in the range
            [0, 2**<number of pins inthe group>). Each pin's value is
            determined by one bit of value with bit 0 indicating the required
            state of teh first pin in ther group, bit 1 the 2nd pin in the
            group and so on.

            Raises Value error if value is out of range or a string that
            cannot be converted to an integer; TypeError is raised if value
            is not a string or a number.
        '''
        value = int(value)
        if value>=0 and value<=self._pin_max_value:
            if self._cached_value==None:
                self._cached_value = ~value & self._pin_max_value
            for bit_number in self._pin_bit_range:
                mask = (1<<bit_number)
                value_bit = value&mask
                if value_bit != (self._cached_value&mask):
                    self._pins[bit_number].write(value_bit)
            self._cached_value = value
        else:
            raise ValueError

class PinListWriter(_PinGroupIOBase, GPIOWriterBase):
    '''
        Concrete GPIOWriterBase implementation for a group of GPIO pins.
        It handles writing 0 or 1 values to the related GPIO pins presented
        as Boolean value elements in an iterable sequence. Each GPIO pin in
        the group will have been exported and set up for output as part of
        the initialisation.
    '''
    def __init__(self, pin_ids):
        '''
            Creates a group of GPIO pins for writing (output) with pin bit
            values expressed to write as Boolean values in an interable
            sequence ordered as per the pin id sequence passed as pin_ids.

            pin_ids should be an iterable sequence of pin id values of the
            pins to be in group. It should contain at least one value
            otherwise a gpioerror.PinGroupIdsInvalidError exception is
            raised. Additionally any exception that might be raised by
            pin.open_pin may be raised other than those relating to bad mode
            values.
            
            On successful return an open pin group object will be open and
            ready to write to. Otherwise it will be closed.
        '''
        super(PinListWriter, self).__init__(pin_ids, 'wN')
        self._cached_value = None
        self._pin_bit_range = range(len(self._pins))

    def write(self, value):
        '''
            Writes the value to the pins in the group.

            The passed value should be an iterable sequence of Boolean
            values (or values convertible to Boolean). Each pin's value is
            determined by one element of value with the first element
            determining the value written to the pin specified by the first
            element of the pin_ids argument passed to __init__ and so on.

            Raises TypeError if value is not an iterable sequence of items
            with the same length as that of the pin_ids argument passed to
            __init__.
        '''
        if isinstance(value, collections.Iterable) and len(value)==len(self._pins):
            if self._cached_value==None:
                self._cached_value = []
                for bit_number in self._pin_bit_range:
                    self._cached_value.append(not value[bit_number])
            for bit_number in self._pin_bit_range:
                if value[bit_number] != self._cached_value[bit_number]:
                    self._pins[bit_number].write(value[bit_number])
            self._cached_value = value
        else:
            raise TypeError


class PinWordReader(_PinGroupIOBase, GPIOReaderBase):
    '''
        Concrete GPIOReaderBase implementation for a group of GPIO pins.
        It handles reading 0 or 1 values from the related GPIO pins presented
        as bits in an integer. Each GPIO pin in the group will have been
        exported and set up for input as part of the initialisation.
    '''
    def __init__(self, pin_ids):
        '''
            Creates a group of GPIO pins for reading (input) with read pin
            bit values expressed as bits in an integer with bit 0 indicating
            the value for the first pin in the group, and bit 1 the next and
            so on. Pins are ordered arounding to the position of their id in
            the pin_ids argument.

            pin_ids should be an iterable sequence of pin id values of the
            pins to be in group. It should contain at least one value
            otherwise a gpioerror.PinGroupIdsInvalidError exception is
            raised. Additionally any exception that might be raised by
            pin.open_pin may be raised other than those relating to bad mode
            values.
            
            On successful return an open pin group object will be open and
            ready to read from. Otherwise it will be closed.
        '''
        super(PinWordReader, self).__init__(pin_ids, 'rN')
        self._pin_bit_range = range(len(self._pins))

    def read(self):
        '''
            Returns an integer whose bits represent the read state of all
            bits in the pin group with bit 0 representing the pin specified by
            the 0th element of pin_ids argument passed to __init__ and so on.

            Note that read polls the pin states and does not wait for any
            state change event to occur.
        '''
        value = 0
        for bit_number in self._pin_bit_range:
            value += (self._pins[bit_number].read() << bit_number)
        return value

class PinListReader(_PinGroupIOBase, GPIOReaderBase):
    '''
        Concrete GPIOReaderBase implementation for a group of GPIO pins.
        It handles reading 0 or 1 values from the related GPIO pins presented
        as Boolean value elements in an iterable sequence. Each GPIO pin in
        the group will have been exported and set up for output as part of
        the initialisation.
    '''
    def __init__(self, pin_ids):
        '''
            Creates a group of GPIO pins for reading (input) with read pin
            bit values expressed as Boolean values in an interable
            sequence ordered as per the pin id sequence passed as pin_ids.

            pin_ids should be an iterable sequence of pin id values of the
            pins to be in group. It should contain at least one value
            otherwise a gpioerror.PinGroupIdsInvalidError exception is
            raised. Additionally any exception that might be raised by
            pin.open_pin may be raised other than those relating to bad mode
            values.
            
            On successful return an open pin group object will be open and
            ready to read from. Otherwise it will be closed.
        '''
        super(PinListReader, self).__init__(pin_ids, 'rN')
        self._pin_bit_range = range(len(self._pins))

    def read(self):
        '''
            Returns a list of Boolean values whose elements represent the
            read state of all bits in the pin group with the 0th element
            representing the pin specified by the 0th element of pin_ids
            argument passed to __init__ and so on.

            Note that read polls the pin states and does not wait for any
            state change event to occur.
        '''
        value = []
        for bit_number in self._pin_bit_range:
            value.append(self._pins[bit_number].read())
        return value

class PinWordBlockingReader(object):#(_PinGroupIOBase, GPIOBlockingReaderBase):
    def __init__(self, pin_ids, blocking_mode):
        pass

class PinListBlockingReader(object):#(_PinGroupIOBase, GPIOBlockingReaderBase):
    def __init__(self, pin_ids, blocking_mode):
        pass

def open_pingroup(pin_ids, mode='rNI'):
    '''
        Open a group of GPIO pins managed as a single entity for IO purposes.

        Factory function creating GPIO pin group objects of appropriate types
        for the requested operational mode.

        pin_ids is sequence of BCM2835 (or BCM2807) GPIO id numbers, probably
        ones connected to the Raspberry Pi P1 connector. They can be PinId type
        instances or int values (which will be validated).

        mode is optional. 
        If passed it should be a string of 0 to 3 characters in length.
        A single mode applies to all pins in a group.
        The first character of the mode string indicates the desired data
        direction: read/input: 'r' or write/output: 'w'
        The second, optional, character indicates the blocking mode:
        block on nothing (non-blocking): 'N', 
        block on rising edge events (0 to 1 transitions): 'R',
        block on falling edge events (1 to 0 transitions): 'F',
        block on events for both edges: 'B'.
        The default is 'N', non-blocking, waiting on no events and is the
        only valid option when opening a pin for writing/output.
        The third optioanl character specifies the format of pin values in
        the group as present to write or returned from read operations.
        I indicates they values are multiplexed into the bits of an integer
        word with bit 0 having the value of the GPIO pin specified by the
        first id in the passed pin_ids sequence, bit 1 the values of the pin
        specified by the next pin id in the passed pin_ids sequence.
        S indicates the values of the pins are presented as discrete Boolean
        values passed or returned in a sequence, with the value of the nth
        element being the value of the GPIO pin having the id that is the nth
        element of the pin_ids parameter.
        The default format is I.
        No mode argument or an empty mode string defaults to read/input,
        non-blocking, integer format - mode 'rNI'

        Value modes strings are:
        'rNI','rNS', 'rRI','rRS', 'rFI','rFS','rBI','rBS','wNI','wNS',
        '', 'r', 'rN', 'rI' : all the same as 'rNI'
        'rS'                : same as 'rNS'
        'rR'                : same as 'rRI'
        'rF'                : same as 'rFI'
        'rB'                : same as 'rBI'
        'w', 'wN', 'wI'     : all the same as 'wNI'
        'wS'                : same as 'wNS'
    '''
    mode_len = len(mode)
    direction_mode = DirectionMode(DirectionMode.read_open_mode())
    edge_mode = BlockMode(BlockMode.non_blocking_open_mode())
    format_mode = FormatMode(FormatMode.integer_open_mode())
    if mode_len >= 1:
        direction_mode = DirectionMode(mode[0])
        if mode_len == 3:
            edge_mode = BlockMode(mode[1])
            format_mode = FormatMode(mode[2])
        elif mode_len == 2: # 2nd char. could be blocking mode or format mode
            try:
                edge_mode = BlockMode(mode[1])
            except PinBlockModeInvalidError:
                try:
                    format_mode = FormatMode(mode[1])
                except PinGroupFormatModeInvalidError:
                    raise PinGroupOpenModeInvalidError
        elif mode_len > 3:
            raise PinGroupOpenModeInvalidError
    if direction_mode.is_write():
        if edge_mode.is_blocking(): # any other blocking mode meaningless for output
            raise PinBlockModeInvalidError
        if format_mode.is_integer():
            return PinWordWriter(pin_ids)
        else:
            return PinListWriter(pin_ids)
    else: # direction mode only read or write...
        assert( direction_mode.is_read() )
        if edge_mode.is_blocking():
            if format_mode.is_integer():
                return PinWordBlockingReader(pin_ids, edge_mode.open_mode_value())
            else:
                return PinListBlockingReader(pin_ids, edge_mode.open_mode_value())
        else:
            if format_mode.is_integer():
                return PinWordReader(pin_ids)
            else:
                return PinListReader(pin_ids)
