'''
    Part of the dibase.rpi.gpio.test package.

    See also: pin-systemtests.py
    
    Single Pin IO support class tests not requiring system
    resources or user interaction.

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

class WaitModeUnitTests(unittest.TestCase):
    def test_not_waitable_open_mode_to_edge_mode_mapping(self):
        not_waitable_wait_mode_value = pin.WaitMode.not_waitable_open_mode()
        self.assertIn(not_waitable_wait_mode_value, pin.WaitMode.all_wait_open_mode_characters())
        self.assertTrue(pin.WaitMode.is_valid_wait_open_mode(not_waitable_wait_mode_value))
        not_waitable_wait_mode = pin.WaitMode(not_waitable_wait_mode_value)
        self.assertEqual(not_waitable_wait_mode.open_mode_value(), pin.WaitMode.not_waitable_open_mode())       
        self.assertEqual(not_waitable_wait_mode.edge_mode_value(), pin.WaitMode.not_waitable_edge_mode())
        self.assertFalse(not_waitable_wait_mode.is_waitable())

    def test_wait_on_rising_edge_open_mode_to_edge_mode_mapping(self):
        wait_on_rising_edge_wait_mode_value = pin.WaitMode.wait_on_rising_edge_open_mode()
        self.assertIn(wait_on_rising_edge_wait_mode_value, pin.WaitMode.all_wait_open_mode_characters())
        self.assertTrue(pin.WaitMode.is_valid_wait_open_mode(wait_on_rising_edge_wait_mode_value))
        wait_on_rising_edge_wait_mode = pin.WaitMode(wait_on_rising_edge_wait_mode_value)
        self.assertEqual(wait_on_rising_edge_wait_mode.open_mode_value(), pin.WaitMode.wait_on_rising_edge_open_mode())       
        self.assertEqual(wait_on_rising_edge_wait_mode.edge_mode_value(), pin.WaitMode.wait_on_rising_edge_edge_mode())
        self.assertTrue(wait_on_rising_edge_wait_mode.is_waitable())

    def test_wait_on_falling_edge_open_mode_to_edge_mode_mapping(self):
        wait_on_falling_edge_wait_mode_value = pin.WaitMode.wait_on_falling_edge_open_mode()
        self.assertIn(wait_on_falling_edge_wait_mode_value, pin.WaitMode.all_wait_open_mode_characters())
        self.assertTrue(pin.WaitMode.is_valid_wait_open_mode(wait_on_falling_edge_wait_mode_value))
        wait_on_falling_edge_wait_mode = pin.WaitMode(wait_on_falling_edge_wait_mode_value)
        self.assertEqual(wait_on_falling_edge_wait_mode.open_mode_value(), pin.WaitMode.wait_on_falling_edge_open_mode())       
        self.assertEqual(wait_on_falling_edge_wait_mode.edge_mode_value(), pin.WaitMode.wait_on_falling_edge_edge_mode())
        self.assertTrue(wait_on_falling_edge_wait_mode.is_waitable())

    def test_wait_on_both_edges_open_mode_to_edge_mode_mapping(self):
        wait_on_both_edges_wait_mode_value = pin.WaitMode.wait_on_both_edges_open_mode()
        self.assertIn(wait_on_both_edges_wait_mode_value, pin.WaitMode.all_wait_open_mode_characters())
        self.assertTrue(pin.WaitMode.is_valid_wait_open_mode(wait_on_both_edges_wait_mode_value))
        wait_on_both_edges_wait_mode = pin.WaitMode(wait_on_both_edges_wait_mode_value)
        self.assertEqual(wait_on_both_edges_wait_mode.open_mode_value(), pin.WaitMode.wait_on_both_edges_open_mode())       
        self.assertEqual(wait_on_both_edges_wait_mode.edge_mode_value(), pin.WaitMode.wait_on_both_edges_edge_mode())
        self.assertTrue(wait_on_both_edges_wait_mode.is_waitable())

    def test_bad_open_mode_values_fail(self):
        max_open_mode_character = max(pin.WaitMode.all_wait_open_mode_characters())
        not_open_mode_character = chr(ord(max_open_mode_character[0])+1)
        not_open_mode_str = pin.WaitMode.all_wait_open_mode_characters()
        bad_open_mode_str = not_open_mode_str[0:2]
        self.assertNotIn( not_open_mode_character
                        , pin.WaitMode.all_wait_open_mode_characters()
                        , "## selected bad open mode character is VALID open mode character!!"
                        )
        self.assertFalse( pin.WaitMode.is_valid_wait_open_mode(not_open_mode_character) )
        self.assertFalse( pin.WaitMode.is_valid_wait_open_mode(bad_open_mode_str) )
        with self.assertRaises( pin.PinWaitModeInvalidError ):
            pin.WaitMode(not_open_mode_character)
        with self.assertRaises( pin.PinWaitModeInvalidError ):
            pin.WaitMode(bad_open_mode_str)

class DirectionModeUnitTests(unittest.TestCase):
    def test_read_open_mode_is_valid(self):
        self.assertTrue(pin.DirectionMode.is_valid_direction_open_mode(pin.DirectionMode.read_open_mode()))

    def test_read_open_mode_is_read(self):
        self.assertTrue( pin.DirectionMode(pin.DirectionMode.read_open_mode()).is_read())
    
    def test_read_open_mode_is_not_write(self):
        self.assertFalse( pin.DirectionMode(pin.DirectionMode.read_open_mode()).is_write())

    def test_read_open_mode_to_direction_mode_mapping(self):
        self.assertEqual( pin.DirectionMode(pin.DirectionMode.read_open_mode())\
                            .direction_mode_value()\
                        , pin.DirectionMode.read_direction_mode()\
                        )

    def test_write_open_mode_is_valid(self):
        self.assertTrue(pin.DirectionMode.is_valid_direction_open_mode(pin.DirectionMode.write_open_mode()))

    def test_write_open_mode_is_write(self):
        self.assertTrue( pin.DirectionMode(pin.DirectionMode.write_open_mode()).is_write())
    
    def test_write_open_mode_is_not_read(self):
        self.assertFalse( pin.DirectionMode(pin.DirectionMode.write_open_mode()).is_read())

    def test_write_open_mode_to_direction_mode_mapping(self):
        self.assertEqual( pin.DirectionMode(pin.DirectionMode.write_open_mode())\
                            .direction_mode_value()\
                        , pin.DirectionMode.write_direction_mode()\
                        )

    def test_bad_open_mode_values_fail(self):
        max_open_mode_character = max(pin.DirectionMode.all_direction_open_mode_characters())
        not_open_mode_character = chr(ord(max_open_mode_character[0])+1)
        not_open_mode_str = pin.DirectionMode.all_direction_open_mode_characters()
        bad_open_mode_str = not_open_mode_str[0:2]
        self.assertNotIn( not_open_mode_character
                        , pin.DirectionMode.all_direction_open_mode_characters()
                        , "## selected bad open mode character is VALID open mode character!!"
                        )
        self.assertFalse( pin.DirectionMode.is_valid_direction_open_mode(not_open_mode_character) )
        self.assertFalse( pin.DirectionMode.is_valid_direction_open_mode(bad_open_mode_str) )
        with self.assertRaises( pin.PinDirectionModeInvalidError ):
            pin.DirectionMode(not_open_mode_character)
        with self.assertRaises( pin.PinDirectionModeInvalidError ):
            pin.DirectionMode(bad_open_mode_str)

if __name__ == '__main__':
    unittest.main()
