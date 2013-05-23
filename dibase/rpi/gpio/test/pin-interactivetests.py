'''
    Part of the dibase.rpi.gpio.test package.

    Interactive platform tests on read/write operations on single GPIO pin
    IO type instances.

    Tests require either observation or GPIO input line state modification
    that probably implies user interaction.               |

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2013 Dibase Limited
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

# Interactive test setup:
# Connect: 
# P1 pin 11 - GPIO_GEN0 - to output indicator such as an LED
# P1 pin 7  - GPIO_GCLK - to an input device such as a switch that can toggle
#                         between low and high states.

class PinIOInteractivePlatformTests(unittest.TestCase):
    __skip = False

    @classmethod
    def setUpClass(cls):
      print "To run these tests please connect the following GPIO pins:"
      print "   P1 pin 11 - GPIO_GEN0 - to an output indicator such as an LED."
      print "   P1 pin 7  - GPIO_GCLK - to an input device such as a switch that can toggle between low and high states."
      option = raw_input("Press enter when ready or Q to quit...")
      if option=='Q' or option=='q':
        PinIOInteractivePlatformTests.__skip = True

    def setUp(self):
      if PinIOInteractivePlatformTests.__skip:
        self.skipTest('User quit request')
      
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids(pin.PinId._get_rpi_major_revision_index()):
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
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        # Read a value from the input pin and check it is False or True.
        # Output this value to the console so if hardware pin GPIO_GCLK
        # on the Raspberry Pi P1 connector is connected to a switch then
        # you can check the read value concurs with the switch state.
        value = a_pin.read()
        self.assertIn(value, [False, True])
        print '\nPinBlockingReader object on GPIO_GCLK: read value:', value
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

    def test_250_blocking_reader_zero_time_out_returns_polled_pin_state(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        a_pin.read() # clear initially signalled notification
        self.assertIn( a_pin.read(0), [False, True] )
        self.assertFalse( a_pin.closed() )

    def test_260_blocking_reader_time_out_expiration_returns_None(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        a_pin.read() # clear initially signalled notification
        self.assertIsNone( a_pin.read(0.001) )
        self.assertFalse( a_pin.closed() )

    def test_300_blocking_reader_wait_both_no_time_out_notifies_and_reads_results_repeatedly_on_any_state_change(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'B' )
        self.assertFalse( a_pin.closed() )
        a_pin.read() # Clear intial signalled event.
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin7) twice (e,g. press and release)..."
        value = a_pin.read()
        self.assertIn(value, [False, True])
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        value = a_pin.read(1000)
        self.assertIn(value, [False, True])
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_350_blocking_reader_wait_rising_edge_no_time_out_notifies_and_reads_results_repeatedly_on_0_1_state_change(self):
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'R' )
        self.assertFalse( a_pin.closed() )
        a_pin.read() # Clear intial signalled event.
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin 7) from 0 to 1 twice (e.g. press, release, press, release)..."
        value = a_pin.read()
        self.assertEqual(value, True)
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        value = a_pin.read()
        self.assertEqual(value, True)
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

    def test_400_blocking_reader_wait_falling_edge_no_time_out_notifies_and_reads_results_repeatedly_on_1_0_state_change(self):
        time.sleep(0.3)
        a_pin = pin.PinBlockingReader( pin.PinId.p1_gpio_gclk(), 'F' )
        self.assertFalse( a_pin.closed() )
        a_pin.read() # Clear intial signalled event.
        print "\nChange value of GPIO_GCLK (Raspberry Pi P1 pin 7) from 1 to 0 twice (e.g. press, release, press, release)..."
        value = a_pin.read()
        self.assertEqual(value, False)
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        value = a_pin.read()
        self.assertEqual(value, False)
        print 'PinBlockingReader object on GPIO_GCLK: read value:', value
        print "Test complete.\n"

if __name__ == '__main__':
    unittest.main()
