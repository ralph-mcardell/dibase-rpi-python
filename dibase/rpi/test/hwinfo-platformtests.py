'''
    Part of the dibase.rpi.test package.

    Platform tests on Raspberry Pi hardware information
 
    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2013 Dibase Limited
    License: dual: GPL or BSD.
'''

import unittest
import sys
if __name__ == '__main__':
    sys.path.insert(0, './../../..')
from dibase.rpi.hwinfo import HwInfo

class HwInfoPlatformTests(unittest.TestCase):
    def test_0010_hw_info_raw_revision_returns_int_value_greater_than_zero(self):
      self.assertIsInstance(HwInfo.raw_revision(),int)
      self.assertTrue(HwInfo.raw_revision()>0)

    def test_0020_hw_info_major_revision_returns_int_value_greater_than_zero(self):
      self.assertIsInstance(HwInfo.major_revision(),int)
      self.assertTrue(HwInfo.major_revision()>0)

    def test_0030_hw_info_major_revision_as_expected_for_raw_revison_value(self):
      self.assertTrue(  (HwInfo.major_revision()==1 and HwInfo.raw_revision()<=3) 
                     or (HwInfo.major_revision()==2 and HwInfo.raw_revision()>3 and HwInfo.raw_revision()<=0xf)
                     or (HwInfo.major_revision()==3 and (HwInfo.raw_revision()==0x10 or HwInfo.raw_revision()==0x12))
                     or (HwInfo.major_revision()==4 and HwInfo.raw_revision()==0x11)
                     or HwInfo.major_revision()==5
                     )

    def test_0040_hw_info_gpio_revision_as_expected_for_major_revison_value(self):
      self.assertTrue(  (HwInfo.gpio_revision()==HwInfo.major_revision())
                     or (HwInfo.gpio_revision()==3 and HwInfo.major_revision()==5)
                     )

if __name__ == '__main__':
    unittest.main()
