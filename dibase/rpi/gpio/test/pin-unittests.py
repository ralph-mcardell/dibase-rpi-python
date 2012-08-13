'''
    Part of the dibase.rpi.gpio.test package.

    See also: pin-systemtests.py
    
    Single Pin IO support class tests not requiring system
    resources or user interaction.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import unittest
import sys
if __name__ == '__main__':
    sys.path.insert(0, './../..')
from gpio import pin

class BlockModeUnitTests(unittest.TestCase):
    def test_non_blocking_open_mode_to_edge_mode_mapping(self):
        non_blocking_wait_mode_value = pin.BlockMode.non_blocking_open_mode()
        self.assertIn(non_blocking_wait_mode_value, pin.BlockMode.all_blocking_open_mode_characters())
        self.assertTrue(pin.BlockMode.is_valid_blocking_open_mode(non_blocking_wait_mode_value))
        non_blocking_wait_mode = pin.BlockMode(non_blocking_wait_mode_value)
        self.assertEqual(non_blocking_wait_mode.open_mode_value(), pin.BlockMode.non_blocking_open_mode())       
        self.assertEqual(non_blocking_wait_mode.edge_mode_value(), pin.BlockMode.non_blocking_edge_mode())
        self.assertFalse(non_blocking_wait_mode.is_blocking())

    def test_block_on_rising_edge_open_mode_to_edge_mode_mapping(self):
        block_on_rising_edge_wait_mode_value = pin.BlockMode.block_on_rising_edge_open_mode()
        self.assertIn(block_on_rising_edge_wait_mode_value, pin.BlockMode.all_blocking_open_mode_characters())
        self.assertTrue(pin.BlockMode.is_valid_blocking_open_mode(block_on_rising_edge_wait_mode_value))
        block_on_rising_edge_wait_mode = pin.BlockMode(block_on_rising_edge_wait_mode_value)
        self.assertEqual(block_on_rising_edge_wait_mode.open_mode_value(), pin.BlockMode.block_on_rising_edge_open_mode())       
        self.assertEqual(block_on_rising_edge_wait_mode.edge_mode_value(), pin.BlockMode.block_on_rising_edge_edge_mode())
        self.assertTrue(block_on_rising_edge_wait_mode.is_blocking())

    def test_block_on_falling_edge_open_mode_to_edge_mode_mapping(self):
        block_on_falling_edge_wait_mode_value = pin.BlockMode.block_on_falling_edge_open_mode()
        self.assertIn(block_on_falling_edge_wait_mode_value, pin.BlockMode.all_blocking_open_mode_characters())
        self.assertTrue(pin.BlockMode.is_valid_blocking_open_mode(block_on_falling_edge_wait_mode_value))
        block_on_falling_edge_wait_mode = pin.BlockMode(block_on_falling_edge_wait_mode_value)
        self.assertEqual(block_on_falling_edge_wait_mode.open_mode_value(), pin.BlockMode.block_on_falling_edge_open_mode())       
        self.assertEqual(block_on_falling_edge_wait_mode.edge_mode_value(), pin.BlockMode.block_on_falling_edge_edge_mode())
        self.assertTrue(block_on_falling_edge_wait_mode.is_blocking())

    def test_block_on_both_edges_open_mode_to_edge_mode_mapping(self):
        block_on_both_edges_wait_mode_value = pin.BlockMode.block_on_both_edges_open_mode()
        self.assertIn(block_on_both_edges_wait_mode_value, pin.BlockMode.all_blocking_open_mode_characters())
        self.assertTrue(pin.BlockMode.is_valid_blocking_open_mode(block_on_both_edges_wait_mode_value))
        block_on_both_edges_wait_mode = pin.BlockMode(block_on_both_edges_wait_mode_value)
        self.assertEqual(block_on_both_edges_wait_mode.open_mode_value(), pin.BlockMode.block_on_both_edges_open_mode())       
        self.assertEqual(block_on_both_edges_wait_mode.edge_mode_value(), pin.BlockMode.block_on_both_edges_edge_mode())
        self.assertTrue(block_on_both_edges_wait_mode.is_blocking())

    def test_bad_open_mode_values_fail(self):
        max_open_mode_character = max(pin.BlockMode.all_blocking_open_mode_characters())
        not_open_mode_character = chr(ord(max_open_mode_character[0])+1)
        not_open_mode_str = pin.BlockMode.all_blocking_open_mode_characters()
        bad_open_mode_str = not_open_mode_str[0:2]
        self.assertNotIn( not_open_mode_character
                        , pin.BlockMode.all_blocking_open_mode_characters()
                        , "## selected bad open mode character is VALID open mode character!!"
                        )
        self.assertFalse( pin.BlockMode.is_valid_blocking_open_mode(not_open_mode_character) )
        self.assertFalse( pin.BlockMode.is_valid_blocking_open_mode(bad_open_mode_str) )
        with self.assertRaises( pin.PinBlockModeInvalidError ):
            pin.BlockMode(not_open_mode_character)
        with self.assertRaises( pin.PinBlockModeInvalidError ):
            pin.BlockMode(bad_open_mode_str)

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
