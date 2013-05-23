'''
    Part of the dibase.rpi.gpio.test package.

    Platform tests on read/write operations on single GPIO pin
    IO type instances.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012,2013 Dibase Limited
    License: dual: GPL or BSD.
'''

import time
import unittest
import sys
if __name__ == '__main__':
# Add path to directory containing the dibase package directory
    sys.path.insert(0, './../../../..') 
from dibase.rpi.gpio import pin
from dibase.rpi.gpio import pinid
from dibase.rpi.gpio import gpioerror as error

class PinWriterPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids(pin.PinId._get_rpi_major_revision_index()):
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWriter( -1 )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWriter( "Nan" )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWriter( 100000 )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWriter( None )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWriter( len(pinid.AllChipPinIdSet.valid_ids()) )

    def test_create_valid_pin_for_writing(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )
        self.assertTrue( a_pin.writable() )
        self.assertFalse( a_pin.readable() )
        self.assertFalse( a_pin.blocking() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_no_explicit_close_closes_on_pin_object_destruction(self):
        ''' Note: failure will be picked up in the tearDown cleanup code '''
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )

    def test_multiple_close_does_nothing_bad(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_file_descriptors_produces_list_of_1_int_on_open_pin(self):
        a_pin = pin.PinWriter(pin.PinId.p1_gpio_gen0())
        self.assertFalse( a_pin.closed() )
        file_descriptor_list = a_pin.file_descriptors()
        self.assertTrue(file_descriptor_list)
        self.assertEqual(len(file_descriptor_list), 1)
        self.assertIsInstance(file_descriptor_list[0], int)
        a_pin.close()

    def test_file_descriptors_returns_empty_list_on_closed_pin(self):
        a_pin = pin.PinWriter(pin.PinId.p1_gpio_gen0())
        a_pin.close()
        self.assertTrue(a_pin.closed())
        file_descriptor_list = a_pin.file_descriptors()
        self.assertFalse(file_descriptor_list)

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinWriter(pin.PinId.p1_gpio_gen0())
        self.assertFalse(a_pin.closed())
        file_descriptor_number = a_pin.fileno()
        self.assertIsNotNone(file_descriptor_number)
        self.assertIsInstance(file_descriptor_number, int)
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinWriter(pin.PinId.p1_gpio_gen0())
        a_pin.close()
        self.assertTrue(a_pin.closed())
        file_descriptor_number = a_pin.fileno()
        self.assertIsNone(file_descriptor_number)

    def test_write_to_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinWriter(pin.PinId.p1_gpio_gen0())
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            a_pin.write(1)

    def test_open_in_with_and_closed_after(self):
        outside_value = None
        with pin.PinWriter( pin.PinId.p1_gpio_gen0() ) as p:
            outside_value = p
            self.assertFalse( p.closed() )
            self.assertFalse( outside_value.closed() )
        self.assertTrue( outside_value.closed() )

class PinReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids(pin.PinId._get_rpi_major_revision_index()):
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinReader( -1 )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinReader( "Nan" )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinReader( 100000 )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinReader( None )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinReader( len(pinid.AllChipPinIdSet.valid_ids()) )

    def test_create_valid_pin_for_reading(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen1() )
        self.assertFalse( a_pin.closed() )
        self.assertFalse( a_pin.writable() )
        self.assertTrue( a_pin.readable() )
        self.assertFalse( a_pin.blocking() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_no_explicit_close_closes_on_pin_object_destruction(self):
        ''' Note: failure will be picked up in the tearDown cleanup code '''
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )

    def test_multiple_close_does_nothing_bad(self):
        a_pin = pin.PinReader(pin.PinId.p1_gpio_gen1())
        self.assertFalse( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_file_descriptors_produces_list_of_1_int_on_open_pin(self):
        a_pin = pin.PinReader(pin.PinId.p1_gpio_gen1())
        self.assertFalse( a_pin.closed() )
        file_descriptor_list = a_pin.file_descriptors()
        self.assertTrue(file_descriptor_list)
        self.assertEqual(len(file_descriptor_list), 1)
        self.assertIsInstance(file_descriptor_list[0], int)
        a_pin.close()

    def test_file_descriptors_returns_empty_list_on_closed_pin(self):
        a_pin = pin.PinReader(pin.PinId.p1_gpio_gen1())
        a_pin.close()
        self.assertTrue(a_pin.closed())
        file_descriptor_list = a_pin.file_descriptors()
        self.assertFalse(file_descriptor_list)

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinReader(pin.PinId.p1_gpio_gen1())
        self.assertFalse(a_pin.closed())
        file_descriptor_number = a_pin.fileno()
        self.assertIsNotNone(file_descriptor_number)
        self.assertIsInstance(file_descriptor_number, int)
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinReader(pin.PinId.p1_gpio_gen1())
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertIsNone(file_descriptor_number)

    def test_write_to_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen1() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            value = a_pin.read()

    def test_open_in_with_and_closed_after(self):
        outside_value = None
        with pin.PinReader( pin.PinId.p1_gpio_gen1() ) as p:
            outside_value = p
            self.assertFalse( p.closed() )
            self.assertFalse( outside_value.closed() )
        self.assertTrue( outside_value.closed() )


class PinBlockingReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids(pin.PinId._get_rpi_major_revision_index()):
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinBlockingReader( -1, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinBlockingReader( "Nan", 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinBlockingReader( 100000, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinBlockingReader( None, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinBlockingReader( len(pinid.AllChipPinIdSet.valid_ids()), 'B' )

    def test_create_valid_pin_for_reading(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )
        self.assertFalse( a_pin.writable() )
        self.assertTrue( a_pin.readable() )
        self.assertTrue( a_pin.blocking() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_no_explicit_close_closes_on_pin_object_destruction(self):
        ''' Note: failure will be picked up in the tearDown cleanup code '''
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )

    def test_multiple_close_does_nothing_bad(self):
        a_pin = pin.PinBlockingReader(pin.PinId.p1_gpio_gen1(), 'B')
        self.assertFalse( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_file_descriptors_produces_list_of_1_int_on_open_pin(self):
        a_pin = pin.PinBlockingReader(pin.PinId.p1_gpio_gen1(), 'B')
        self.assertFalse( a_pin.closed() )
        file_descriptor_list = a_pin.file_descriptors()
        self.assertTrue(file_descriptor_list)
        self.assertEqual(len(file_descriptor_list), 1)
        self.assertIsInstance(file_descriptor_list[0], int)
        a_pin.close()

    def test_file_descriptors_returns_empty_list_on_closed_pin(self):
        a_pin = pin.PinBlockingReader(pin.PinId.p1_gpio_gen1(), 'B')
        a_pin.close()
        self.assertTrue(a_pin.closed())
        file_descriptor_list = a_pin.file_descriptors()
        self.assertFalse(file_descriptor_list)

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinBlockingReader(pin.PinId.p1_gpio_gen1(), 'B')
        self.assertFalse(a_pin.closed())
        file_descriptor_number = a_pin.fileno()
        self.assertIsNotNone(file_descriptor_number)
        self.assertIsInstance(file_descriptor_number, int)
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinBlockingReader(pin.PinId.p1_gpio_gen1(), 'B')
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertIsNone(file_descriptor_number)

    def test_read_to_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gen1(), 'B' )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            value = a_pin.read()

    def test_open_in_with_and_closed_after(self):
        outside_value = None
        with pin.PinBlockingReader( pin.PinId.p1_gpio_gen1(), 'B' ) as p:
            outside_value = p
            self.assertFalse( p.closed() )
            self.assertFalse( outside_value.closed() )
        self.assertTrue( outside_value.closed() )

class OpenFunctionPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids(pin.PinId._get_rpi_major_revision_index()):
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_open_pin_for_writing_creates_PinWriter(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'w'),pin.PinWriter)

    def test_open_pin_for_writing_nowaitmode_creates_PinWriter(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'wN'),pin.PinWriter)

    def test_open_pin_for_writing_somewaitmode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'wR'),pin.PinWriter)
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'wF'),pin.PinWriter)
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'wB'),pin.PinWriter)
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'w#'),pin.PinWriter)

    def test_open_pin_for_reading_creates_PinReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'r'),pin.PinReader)

    def test_open_pin_for_reading_nowaitmode_creates_creates_PinReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rN'),pin.PinReader)

    def test_open_pin_default_mode_creates_PinReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0()),pin.PinReader)

    def test_open_pin_empty_mode_creates_PinReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),''),pin.PinReader)

    def test_open_pin_for_reading_waitonfallingedge_creates_PinBlockingReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rF'),pin.PinBlockingReader)

    def test_open_pin_for_reading_waitonrisingedge_creates_PinBlockingReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rR'),pin.PinBlockingReader)

    def test_open_pin_for_reading_waitonbothedges_creates_PinBlockingReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rB'),pin.PinBlockingReader)

    def test_open_pin_for_reading_badwaitmode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rX'),pin.PinWriter)

    def test_open_pin_bad_rw_mode_fails(self):
        with self.assertRaises( error.PinDirectionModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'a'),pin.PinWriter)

    def test_open_pin_bad_mode_string_fails(self):
        with self.assertRaises( error.PinOpenModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rN+'),pin.PinWriter)

if __name__ == '__main__':
    unittest.main()
