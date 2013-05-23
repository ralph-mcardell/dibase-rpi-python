'''
    Part of the dibase.rpi.gpio package.

    Encapsulation of GPIO pin id values and supporting clases.
    
    Underlying GPIO pin ids are those used by the Linux gpiolib and used
    to identify a device's GPIO pins in the Linux sys filesystem GPIO
    sub-tree. They are likely different to the actual pin numbers on the
    Raspberry Pi's BCM2835 SoC but are the same as GPIO pin numbers shown in
    BCM2835 peripheral documentation (e.g. 'BCM2835 ARM Peripherals' tables
    6-2 through to 6-7) and the Raspberry Pi circuit diagram. They also differ
    from the Raspberry Pi's P1 connectors pin assignments - which only support
    a subset of the GPIO pins provided by the BCM2835 SoC.
    
    The pin id support provides a PinId class that sub-classes int, only 
    allowing values that represent GPIO pin id values valid for use with a
    Raspberry Pi, either any GPIO pin id value that is valid for the BCM2835
    SoC or, more commonly, the subset of values representing GPIO pins
    connected to the Raspberry Pi's P1 connector. Provides various factory
    class methods to produce valid GPIO pin ids.
 
    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''
from gpioerror import PinIdInvalidError
from gpioerror import PinIdInvalidRevisionError
from .. import hwinfo

class PinIdValidator(object):
    '''
        Unary predicate functor type.

        Construct an instance from a set of integer pin id valid values
        to which the in operation can be applied (e.g. a set, frozenset,
        range, ...).

        When called an instance returns True if the value under validation
        can be converted to an int AND is in the set of valid values passed
        to the constructor.
    '''
    def __init__(self, valid_ids):
        '''
            Construct PinIdValidator functor instance.
            
            valid_ids is an set of valid pin id integer values to which the
            in operation can be applied.
        '''
        self.__valid_ids = valid_ids

    def __call__(self, pin_id):
        '''
            Unary predicate. Validates a pin id value.

            pin_id is the pin id value to validate

            Returns True if pin_id is convertable to int AND is in the set
            of valid values passed to the functor constructor.
            Otherwise returns False.
        '''
        try:
            pin_id = int(pin_id) # can we convert id to an int?
            if (pin_id in self.__valid_ids ):
                return True
        except StandardError:
            pass
        return False
    
class RPiPinIdSet(object):
    '''
        Provides validation and pin mapping facilities for the set of pin
        ids for GPIO lines connected to the Raspberry Pi P1 connector.
    '''
    __RPI_P1_PIN_TO_IDS = ( # Raspberry Pi revision 1 P1 pins GPIO pins
                            (None,None,None,   0,None,   1,None,   4,  14
                            ,None,  15,  17,  18,  21,None,  22,  23,None
                            ,  24,  10,None,   9,  25,  11,   8,None,   7
                            )
                          , # Raspberry Pi revision 2 P1 pins GPIO pins
                            (None,None,None,   2,None,   3,None,   4,  14
                            ,None,  15,  17,  18,  27,None,  22,  23,None
                            ,  24,  10,None,   9,  25,  11,   8,None,   7
                            )                           
                          )
    __RPI_P5_PIN_TO_IDS = ( # Raspberry Pi revision 1 P5 pins GPIO pins
                            ( None,None,None,None,None,None,None,None,None)
                          , # Raspberry Pi revision 2 P5 pins GPIO pins
                            (None,None,None,  28,  29,  30,  31,None,None)
                          )

    __RPI_IDS = ( # Raspberry Pi revision 1 P1 and P5 pins
                  frozenset( ( set(__RPI_P1_PIN_TO_IDS[0])
                             | set(__RPI_P5_PIN_TO_IDS[0])
                             ) - frozenset([None]) 
                           )
                , # Raspberry Pi revision 2 P1 and P5 pins
                  frozenset( ( set(__RPI_P1_PIN_TO_IDS[1]) 
                             | set(__RPI_P5_PIN_TO_IDS[1]) 
                             ) - frozenset([None]) 
                           )
                )

    @classmethod
    def validator( cls, rev_idx ):
        '''
            Returns a PinIdValidator instance for the Raspberry Pi P1 connector
            GPIO pin id value set.
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)
       '''
        return PinIdValidator( RPiPinIdSet.valid_ids(rev_idx) )

    @classmethod
    def valid_ids( cls, rev_idx ):
        '''
            Returns set of GPIO pin ids for GPIO lines connected to the
            Raspberry Pi P1 connector.
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)
        '''
        return RPiPinIdSet.__RPI_IDS[rev_idx]

    @classmethod
    def p1_pin_to_gpio_pin_id( cls, p1_pin_number, rev_idx ):
        '''
            Returns the GPIO pin id value assigned to a Raspberry Pi P1
            connector pin. 

            p1_pin_number is a Raspberry Pi P1 connector pin number in the
            range [1, 26].
            
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)

            Note that not all P1 connector pins have an associated GPIO pin
            id - these P1 pin numbers will return None. If an out of range
            or non integer value is passed then None is returned.  
        '''
        try:
            p1_pin_number = int(p1_pin_number)
            if ( p1_pin_number not in
                    range(0,len(RPiPinIdSet.__RPI_P1_PIN_TO_IDS[rev_idx])) ):
                return None
        except StandardError:
            return None
        return RPiPinIdSet.__RPI_P1_PIN_TO_IDS[rev_idx][p1_pin_number]

    @classmethod
    def p5_pin_to_gpio_pin_id( cls, p5_pin_number, rev_idx ):
        '''
            Returns the GPIO pin id value assigned to a Raspberry Pi P5
            connector pin. 

            p5_pin_number is a Raspberry Pi P1 connector pin number in the
            range [1, 8].
            
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)

            Note that not all P5 connector pins have an associated GPIO pin
            id - these P5 pin numbers will return None. If an out of range
            or non integer value is passed then None is returned.  
        '''
        try:
            p5_pin_number = int(p5_pin_number)
            if ( p5_pin_number not in
                    range(0,len(RPiPinIdSet.__RPI_P5_PIN_TO_IDS[rev_idx])) ):
                return None
        except StandardError:
            return None
        return RPiPinIdSet.__RPI_P5_PIN_TO_IDS[rev_idx][p5_pin_number]

    @classmethod
    def p1_pin_to_gpio_pin_id_tuple( cls, rev_idx ):
        '''
            Returns tuple used to map Raspberry Pi P1 connector pins numbers
            as index into the tuple to GPIO pin id element values. Not all P1
            pins are connected to GPIO pins - these elements have a None value.
            Mostly for use by tests
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)
        '''
        return RPiPinIdSet.__RPI_P1_PIN_TO_IDS[rev_idx]

    @classmethod
    def p5_pin_to_gpio_pin_id_tuple( cls, rev_idx ):
        '''
            Returns tuple used to map Raspberry Pi P5 connector pins numbers
            as index into the tuple to GPIO pin id element values. Not all P5
            pins are connected to GPIO pins - these elements have a None value.
            Mostly for use by tests
            rev_idx is the Raspberry Pi board revision index (zero based value
            that is one less than the major board revision value)
        '''
        return RPiPinIdSet.__RPI_P5_PIN_TO_IDS[rev_idx]

class AllChipPinIdSet(object):
    '''
        Provides validation information for the set of all BCM2835 GPIO pin ids
    '''
    __NUM_IDS = 54

    @classmethod
    def validator( cls ):
        '''
            Returns a PinIdValidator instance for all BCM2835 chip GPIO
            pin id value set.
        '''
        return PinIdValidator( AllChipPinIdSet.valid_ids() )

    @classmethod
    def valid_ids( cls ):
        '''
            Returns set of GPIO pin ids for the BCM2835 chip.
        '''
        return range(0, AllChipPinIdSet.__NUM_IDS)

class PinId(int):
    '''
        A sub-class of int that only supports a specific (small) subset of
        int values, as detemined by a validator type instance that is a
        callable unary predicate that returns True if the value is in this
        subset or False otherwise. The subset of values represent GPIO pin id
        values that can be used with Linux kernel gpiolib based facilities
        such as the user space sys filesystem GPIO support.
        
        Provides specific support for GPIO pin ids for GPIO lines connected
        to Raspberry Pi P1 connectors.
    '''

    def __new__( cls, pin_id, validator ):
        '''
            Checks id for validity and if OK creates an int having the
            id value, otherwise throws a PinIdInvalidError.
            
            pin_id should be convertable to an int.

            Returns True if that value is convertable to an int and also
            has a permitted pin value.
        '''
        if ( validator(pin_id) ):
            return super(PinId, cls).__new__(cls, pin_id)
        raise PinIdInvalidError

    @classmethod
    def gpio( cls, pin_id ):
        '''
            Returns a PinId instance for GPIO lines connected to the
            Raspberry Pi P1 connector with the value id - which represents
            the pin id values used by the Linux sys filesystem GPIO support.
        '''
        return PinId( pin_id, RPiPinIdSet.validator(PinId._get_rpi_major_revision_index()) )

    @classmethod
    def any_chip_gpio( cls, pin_id ):
        '''
            Returns a PinId instance for any of the GPIO lines supported by
            the BCM2835 chip with the value pin_id - which represents the pin
            id values used by the Linux sys filesystem GPIO support.
        '''
        return PinId( pin_id, AllChipPinIdSet.validator() )

    @classmethod
    def p1_pin( cls, pin ):
        '''
            Create a sys filesystem GPIO pin id for the equivalent pin
            number of the Raspberry Pi P1 26 pin header connector.
            
            pin is a Raspberry Pi P1 connector pin number in the range [1, 26].
            Note that not all values in this range are valid as some P1 pins
            are for other purposes or not to be used at all.
            
            Invalid pin values, either bad or out of range values or P1 pin
            numbers that are not connected to GPIO lines will raise a
            PinIdInvalidError.
        '''
        pin_id = RPiPinIdSet.p1_pin_to_gpio_pin_id(pin,PinId._get_rpi_major_revision_index())
        if ( pin_id == None ):
            raise PinIdInvalidError
        return PinId.gpio(pin_id)

    @classmethod
    def p5_pin( cls, pin ):
        '''
            Create a sys filesystem GPIO pin id for the equivalent pin
            number of the Raspberry Pi P5 8 pin header connector.
            
            pin is a Raspberry Pi P5 connector pin number in the range [1, 8].
            Note that not all values in this range are valid as some P5 pins
            are for other purposes or not to be used at all, and P5 only exists
            on major revision 2 boards (and later?)
            
            Invalid pin values, either bad or out of range values or P5 pin
            numbers that are not connected to GPIO lines will raise a
            PinIdInvalidError.
        '''
        pin_id = RPiPinIdSet.p5_pin_to_gpio_pin_id(pin,PinId._get_rpi_major_revision_index())
        if ( pin_id == None ):
            raise PinIdInvalidError
        return PinId.gpio(pin_id)

    @classmethod
    def p1_sda( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SDA pin '''
        return PinId.p1_pin( 3 )

    @classmethod
    def p1_scl( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SCL pin '''
        return PinId.p1_pin( 5 )

    @classmethod
    def p1_gpio_gclk( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GCLK pin '''
        return PinId.p1_pin( 7 )

    @classmethod
    def p1_txd( cls ):
        '''Return PinId instance representing Raspberry Pi P1 TXD0 pin '''
        return PinId.p1_pin( 8 )

    @classmethod
    def p1_rxd( cls ):
        '''Return PinId instance representing Raspberry Pi P1 RXD0 pin '''
        return PinId.p1_pin( 10 )

    @classmethod
    def p1_gpio_gen0( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN0 pin '''
        return PinId.p1_pin( 11 )

    @classmethod
    def p1_gpio_gen1( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN1 pin '''
        return PinId.p1_pin( 12 )

    @classmethod
    def p1_gpio_gen2( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN2 pin '''
        return PinId.p1_pin( 13 )

    @classmethod
    def p1_gpio_gen3( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN3 pin '''
        return PinId.p1_pin( 15 )

    @classmethod
    def p1_gpio_gen4( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN4 pin '''
        return PinId.p1_pin( 16 )

    @classmethod
    def p1_gpio_gen5( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN5 pin '''
        return PinId.p1_pin( 18 )

    @classmethod
    def p1_spi_mosi( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SPI_MOSI pin '''
        return PinId.p1_pin( 19 )

    @classmethod
    def p1_spi_miso( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SPI_MISO pin '''
        return PinId.p1_pin( 21 )

    @classmethod
    def p1_gpio_gen6( cls ):
        '''Return PinId instance representing Raspberry Pi P1 GPIO_GEN6 pin '''
        return PinId.p1_pin( 22 )

    @classmethod
    def p1_spi_sclk( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SPI_SCLK pin '''
        return PinId.p1_pin( 23 )

    @classmethod
    def p1_spi_ce0_n( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SPI_CE0_N pin '''
        return PinId.p1_pin( 24 )

    @classmethod
    def p1_spi_ce1_n( cls ):
        '''Return PinId instance representing Raspberry Pi P1 SPI_CE1_N pin '''
        return PinId.p1_pin( 26 )
    
    @classmethod
    def p5_gpio_gen7( cls ):
        '''Return PinId instance representing Raspberry Pi P5 GPIO_GEN7 pin '''
        return PinId.p5_pin( 3 )
    
    @classmethod
    def p5_gpio_gen8( cls ):
        '''Return PinId instance representing Raspberry Pi P5 GPIO_GEN8 pin '''
        return PinId.p5_pin( 4 )
    
    @classmethod
    def p5_gpio_gen9( cls ):
        '''Return PinId instance representing Raspberry Pi P5 GPIO_GEN9 pin '''
        return PinId.p5_pin( 5 )
    
    @classmethod
    def p5_gpio_gen10( cls ):
        '''Return PinId instance representing Raspberry Pi P5 GPIO_GEN10 pin '''
        return PinId.p5_pin( 6 )
    
    @classmethod
    def _set_rpi_major_revision(cls, revision):
      ''' Sets internal class attibute specifying the major Raspberry Pi
          board revision. Note: exposed mainly for testing purposes.

          Param   revision  Small positive value representing a Raspberry Pi
                            board major revision number. As of May 2013
                            values of 1 or 2 are valid
      '''
      if PinIdValidator({1,2})(revision):
        PinId.__rpi_revision_index = revision - 1 # 0 based version of revision
      else:
        raise PinIdInvalidRevisionError()

    @classmethod
    def _get_rpi_major_revision_index(cls):
      ''' Return the internal class attibute specifying the major Raspberry Pi
          board revision as a 0 based index value. If this value is not set
          then will attempt to set it by passing the result of 
          dibase.rpi.hwinfo.HwInfo.major_revision() to
          PinId._set_rpi_major_revision.

          Returns Revision index, a small 0 based positive integer value
                  representing a Raspberry Pi board major revision number. 
                  As of May 2013 returned value may be 0 or 1.
      '''
      if PinId.__rpi_revision_index==None:
        PinId._set_rpi_major_revision(hwinfo.HwInfo.major_revision())
      return PinId.__rpi_revision_index

    __rpi_revision_index = None
