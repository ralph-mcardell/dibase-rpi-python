'''
    Part of the dibase.rpi.gpio.test package.

    System tests on read/write operations on single GPIO pin
    IO type instances.
    
    ---------------------------------------------------------------
    | NOTE: Some tests require GPIO input line state modification |
    |       that probably implies user interaction.               |
    ---------------------------------------------------------------

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import time
import unittest
import sys
if __name__ == '__main__':
    sys.path.insert(0, './../..')
from gpio import pin
from gpio import pinid
from gpio import gpioerror as error

class PinWriterSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
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

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertNotEqual(file_descriptor_number, None)
        self.assertIsInstance( file_descriptor_number, int )
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertEqual(file_descriptor_number, None)

    def test_write_to_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
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

class PinReaderSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
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
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen1() )
        self.assertFalse( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen1() )
        self.assertFalse( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertNotEqual(file_descriptor_number, None)
        self.assertIsInstance( file_descriptor_number, int )
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gen1() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertEqual(file_descriptor_number, None)

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


class PinWaitableReaderSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWaitableReader( -1, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWaitableReader( "Nan", 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWaitableReader( 100000, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWaitableReader( None, 'B' )
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin = pin.PinWaitableReader( len(pinid.AllChipPinIdSet.valid_ids()), 'B' )

    def test_create_valid_pin_for_reading(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )
        self.assertFalse( a_pin.writable() )
        self.assertTrue( a_pin.readable() )
        self.assertTrue( a_pin.blocking() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_no_explicit_close_closes_on_pin_object_destruction(self):
        ''' Note: failure will be picked up in the tearDown cleanup code '''
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )

    def test_multiple_close_does_nothing_bad(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        a_pin.close()
        self.assertTrue( a_pin.closed() )

    def test_fileno_produces_int_on_open_pin(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        self.assertFalse( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertNotEqual(file_descriptor_number, None)
        self.assertIsInstance( file_descriptor_number, int )
        a_pin.close()

    def test_fileno_produces_None_on_closed_pin(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        file_descriptor_number = a_pin.fileno()
        self.assertEqual(file_descriptor_number, None)

    def test_write_to_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            value = a_pin.read()

    def test_wait_on_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            value = a_pin.wait()

    def test_reset_on_closed_pin_raises_ValueError_exception(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' )
        a_pin.close()
        self.assertTrue( a_pin.closed() )
        with self.assertRaises( ValueError ):
            a_pin.reset()

    def test_open_in_with_and_closed_after(self):
        outside_value = None
        with pin.PinWaitableReader( pin.PinId.p1_gpio_gen1(), 'B' ) as p:
            outside_value = p
            self.assertFalse( p.closed() )
            self.assertFalse( outside_value.closed() )
        self.assertTrue( outside_value.closed() )

class OpenFunctionSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
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

    def test_open_pin_for_reading_waitonfallingedge_creates_PinWaitableReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rF'),pin.PinWaitableReader)

    def test_open_pin_for_reading_waitonrisingedge_creates_PinWaitableReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rR'),pin.PinWaitableReader)

    def test_open_pin_for_reading_waitonbothedges_creates_PinWaitableReader(self):
        self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rB'),pin.PinWaitableReader)

    def test_open_pin_for_reading_badwaitmode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rX'),pin.PinWriter)

    def test_open_pin_bad_rw_mode_fails(self):
        with self.assertRaises( error.PinDirectionModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'a'),pin.PinWriter)

    def test_open_pin_bad_mode_string_fails(self):
        with self.assertRaises( error.PinOpenModeInvalidError ):
            self.assertIsInstance(pin.open_pin(pin.PinId.p1_gpio_gen0(),'rN+'),pin.PinWriter)

class XPinIOInteractiveSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_050_write_to_open_pin_allows_various_values_in_on_off_on_off_etc_sequence(self):
        a_pin = pin.PinWriter( pin.PinId.p1_gpio_gen0() )
        self.assertFalse( a_pin.closed() )
        # if hardware pin GPIO_GEN0 on the Raspberry Pi P1 connector is
        # connected to an indicator such as as LED that lights for a 1 output
        # then it should flash ON OFF ON OFF ON OFF ON OFF in approximately a
        # .2 second cycle time.
        print "\nToggling GPIO_GEN0 (Raspberry Pi P1 pin 11): ON OFF ON OFF ON OFF ON OFF ..."
        time.sleep(1.5)
        a_pin.write(1)
        time.sleep(0.2)
        a_pin.write(0)
        time.sleep(0.2)
        a_pin.write(True)
        time.sleep(0.2)
        a_pin.write(False)
        time.sleep(0.2)
        a_pin.write(23)
        time.sleep(0.2)
        a_pin.write(None)
        time.sleep(0.2)
        a_pin.write('1')
        time.sleep(0.2)
        a_pin.write('0')
        time.sleep(0.2)
        a_pin.close()
        print "Test complete.\n"

    def test_100_read_from_open_pin_non_blocking_returns_True_or_False(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gclk() )
        self.assertFalse( a_pin.closed() )
        # Read a value from the input pin and check it is False or True.
        # Output this value to the console so if hardware pin GPIO_GCLK
        # on the Raspberry Pi P1 connector is connected to a switch then
        # you can check the read value concurs with the switch state.
        value = a_pin.read()
        self.assertIn(value, [False, True])
        print '\nPinReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_150_read_from_open_pin_blocking_returns_True_or_False(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        # Read a value from the input pin and check it is False or True.
        # Output this value to the console so if hardware pin GPIO_GCLK
        # on the Raspberry Pi P1 connector is connected to a switch then
        # you can check the read value concurs with the switch state.
        value = a_pin.read()
        self.assertIn(value, [False, True])
        print '\nPinWaitableReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_200_read_from_open_pin_non_blocking_more_than_once_returns_expected_results(self):
        a_pin = pin.PinReader( pin.PinId.p1_gpio_gclk() )
        self.assertFalse( a_pin.closed() )
        print "\nSet GPIO_GCLK (Raspberry Pi P1 pin7) HIGH..."
        time.sleep(3.0)
        value = a_pin.read()
        self.assertTrue(value)
        print "Set GPIO_GCLK (Raspberry Pi P1 pin7) LOW..."
        time.sleep(3.0)
        value = a_pin.read()
        self.assertFalse(value)
        print "Test complete.\n"

    def test_250_blocking_reader_time_out_expiration_returns_None(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        a_pin.reset() # clear initially signalled notification
        self.assertIsNone( a_pin.wait(0.001) )
        self.assertFalse( a_pin.closed() )

    def test_300_blocking_reader_wait_both_no_time_out_notifies_and_reads_results_repeatedly_on_any_state_change(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin7) twice (e,g. press and release)..."
        a_pin.reset()
        changed_object = a_pin.wait()
        self.assertIs( changed_object, a_pin )
        value = a_pin.read()
        self.assertIn(value, [False, True])
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        time.sleep(0.05)
        a_pin.reset()
        changed_object = a_pin.wait(1000)
        self.assertIs( changed_object, a_pin )
        value = a_pin.read()
        self.assertIn(value, [False, True])
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_350_blocking_reader_wait_rising_edge_no_time_out_notifies_and_reads_results_repeatedly_on_0_1_state_change(self):
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gclk(), 'R' )
        self.assertFalse( a_pin.closed() )
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin 7) from 0 to 1 twice (e.g. press, release, press, release)..."
        a_pin.reset()
        a_pin.wait()
        value = a_pin.read()
        self.assertEqual(value, True)
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        a_pin.reset()
        a_pin.wait()
        value = a_pin.read()
        self.assertEqual(value, True)
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_400_blocking_reader_wait_falling_edge_no_time_out_notifies_and_reads_results_repeatedly_on_1_0_state_change(self):
        time.sleep(0.3)
        a_pin = pin.PinWaitableReader( pin.PinId.p1_gpio_gclk(), 'F' )
        self.assertFalse( a_pin.closed() )
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin 7) from 1 to 0 twice (e.g. press, release, press, release)..."
        a_pin.reset()
        a_pin.wait()
        value = a_pin.read()
        self.assertEqual(value, False)
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        a_pin.reset()
        a_pin.wait()
        value = a_pin.read()
        self.assertEqual(value, False)
        self.assertEqual( a_pin.read(), value )
        print 'PinWaitableReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

if __name__ == '__main__':
    unittest.main()
