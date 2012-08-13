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
from gpio import pingroup


class FormatModeUnitTests(unittest.TestCase):
    def test_integer_open_mode_is_valid(self):
        self.assertTrue(pingroup.FormatMode.is_valid_format_open_mode(pingroup.FormatMode.integer_open_mode()))

    def test_integer_open_mode_is_integer(self):
        self.assertTrue(pingroup.FormatMode(pingroup.FormatMode.integer_open_mode()).is_integer())
    
    def test_integer_open_mode_is_not_sequence(self):
        self.assertFalse(pingroup.FormatMode(pingroup.FormatMode.integer_open_mode()).is_sequence())

    def test_sequence_open_mode_is_valid(self):
        self.assertTrue(pingroup.FormatMode.is_valid_format_open_mode(pingroup.FormatMode.sequence_open_mode()))

    def test_sequence_open_mode_is_sequence(self):
        self.assertTrue(pingroup.FormatMode(pingroup.FormatMode.sequence_open_mode()).is_sequence())
    
    def test_sequence_open_mode_is_not_integer(self):
        self.assertFalse(pingroup.FormatMode(pingroup.FormatMode.sequence_open_mode()).is_integer())

    def test_bad_open_mode_values_fail(self):
        max_open_mode_character = max(pingroup.FormatMode.all_format_open_mode_characters())
        not_open_mode_character = chr(ord(max_open_mode_character[0])+1)
        not_open_mode_str = pingroup.FormatMode.all_format_open_mode_characters()
        bad_open_mode_str = not_open_mode_str[0:2]
        self.assertNotIn( not_open_mode_character
                        , pingroup.FormatMode.all_format_open_mode_characters()
                        , "## selected bad open mode character is VALID open mode character!!"
                        )
        self.assertFalse(pingroup.FormatMode.is_valid_format_open_mode(not_open_mode_character))
        self.assertFalse(pingroup.FormatMode.is_valid_format_open_mode(bad_open_mode_str))
        with self.assertRaises(pingroup.PinGroupFormatModeInvalidError):
            pingroup.FormatMode(not_open_mode_character)
        with self.assertRaises(pingroup.PinGroupFormatModeInvalidError):
            pingroup.FormatMode(bad_open_mode_str)

if __name__ == '__main__':
    unittest.main()

