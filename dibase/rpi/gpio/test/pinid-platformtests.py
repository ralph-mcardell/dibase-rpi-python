'''
    Part of the dibase.rpi.gpio.test package.

    GPIO pin id support classes' platform tests.
    Underlying GPIO pin ids are those used by the Linux gpiolib and used
    to identify a device's GPIO pins in the Linux sys filesystem GPIO
    sub-tree.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import unittest

import sys
if __name__ == '__main__':
# Add path to directory containing the dibase package directory
    sys.path.insert(0, './../../../..') 
from dibase.rpi.gpio import pinid

class PinIdRPiPlatforrmTestCases(unittest.TestCase):

    def test_0000_get_rpi_major_revision_index_returns_zero_or_positive_int(self):
      returned_rev_index = pinid.PinId._get_rpi_major_revision_index()
      self.assertIsNotNone(returned_rev_index)
      self.assertIsInstance(returned_rev_index,int)
      self.assertTrue(returned_rev_index>=0)

    def test_0020_PinId_value_of_p1_sda_0_or_2(self):
      rev_index = pinid.PinId._get_rpi_major_revision_index()
      p1_sda_gpio_id = pinid.PinId.p1_sda()
      self.assertTrue((rev_index==0 and p1_sda_gpio_id==0) or p1_sda_gpio_id==2)

if __name__ == '__main__':
    unittest.main()
