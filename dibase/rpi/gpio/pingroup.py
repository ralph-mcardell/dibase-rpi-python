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

class PinWordWriter(GPIOWriterBase):
    def __init__(self, pin_ids):
        self.__pins = []
        if not (pin_ids and isinstance(pin_ids, collections.Iterable)):
            raise PinGroupIdsInvalidError
        for id in pin_ids:
            try:
                p = open_pin(id, 'wN')
                self.__pins.append(p)
            except GPIOError, e:
            # Close open pins ASAP - do not wait for __del__ to be called
                for p in self.__pins:
                    p.close()
                self.__pins = []
                raise e
        self.__cached_value = None

    def __del__(self):
        '''Calls close to try to ensure pin group is cleanly freed up'''
        if self.__pins:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''Calls close to ensure pin group is cleanly freed up'''
        self.close()

    def close(self):
        if not self.closed():
            for p in self.__pins:
                p.close()

    def closed(self):
        return self.__pins[0].closed()

    def file_descriptors(self):
        if self.closed():
            return []
        else:
            fds = []
            for p in self.__pins:
                fds.append(p.fileno())
            return fds
        
    def write(self, value):
        value = int(value)
        if ( value>=0 and value<2**len(self.__pins) ):
            if self.__cached_value==None:
                self.__cached_value = ~value & ((2**len(self.__pins))-1)
            for bit_number in range(len(self.__pins)):
                if ((value >> bit_number)&1) != ((self.__cached_value >> bit_number)&1):
                    self.__pins[bit_number].write(((value >> bit_number)&1)!=0)
            self.__cached_value = value
        else:
            raise ValueError

class PinListWriter(object):#(GPIOWriterBase):
    def __init__(self, pin_ids):
        pass

class PinWordReader(object):#(GPIOReaderBase):
    def __init__(self, pin_ids):
        pass

class PinListReader(object):#(GPIOReaderBase):
    def __init__(self, pin_ids):
        pass

class PinWordBlockingReader(object):#(GPIOBlockingReaderBase):
    def __init__(self, pin_ids, blocking_mode):
        pass

class PinListBlockingReader(object):#(GPIOBlockingReaderBase):
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
