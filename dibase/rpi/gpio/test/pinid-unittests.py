'''
    Part of the dibase.rpi.gpio.test package.

    GPIO pin id support classes' unit tests.
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

class PinIdValidatorTestCases(unittest.TestCase):
  def test_with_range(self):
      validator = pinid.PinIdValidator( range(0,10) )
      self.assertTrue( validator(0) )
      self.assertTrue( validator(9) )
      self.assertFalse( validator(-1) )
      self.assertFalse( validator(10) )
      self.assertFalse( validator(None) )
      self.assertFalse( validator("Nan") )

  def test_with_frozenset(self):
      validator = pinid.PinIdValidator( frozenset([0,1,2,3,4,5,6,7,8,9]) )
      self.assertTrue( validator(0) )
      self.assertTrue( validator(9) )
      self.assertFalse( validator(-1) )
      self.assertFalse( validator(10) )
      self.assertFalse( validator(None) )
      self.assertFalse( validator("Nan") )

class AllChipPinIdSetUnitTests(unittest.TestCase):
  def test_all_valid_chip_pin_ids_pass_validation(self):
    for v in pinid.AllChipPinIdSet.valid_ids():
      self.assertTrue( pinid.AllChipPinIdSet.validator()(v) )

  def test_invalid_initialisation_values_cause_instance_creation_fail(self):
    self.assertFalse( pinid.AllChipPinIdSet.validator()(-1) )
    self.assertFalse( pinid.AllChipPinIdSet.validator()("NaN") )
    self.assertFalse( pinid.AllChipPinIdSet.validator()(100000) )
    self.assertFalse( pinid.AllChipPinIdSet.validator()(None) )

class RPiPinIdSetTestCases(unittest.TestCase):
  def setUp(self):
    self.rev_idx_range = range(4); # values [0,3] in range

  def test_invariant_all_valid_rpi_pin_ids_are_also_valid_chip_pin_ids(self):
    for idx in self.rev_idx_range:
      for v in pinid.RPiPinIdSet.valid_ids(idx):
        self.assertIn( v, pinid.AllChipPinIdSet.valid_ids() )

  def test_all_valid_rpi_pin_ids_pass_validation(self):
    for idx in self.rev_idx_range:
      rpi_pin_id_validator = pinid.RPiPinIdSet.validator(idx)
      for v in pinid.RPiPinIdSet.valid_ids(idx):
        self.assertTrue( rpi_pin_id_validator(v) )

  def test_all_valid_chip_pin_ids_that_are_invalid_rpi_pin_ids_fail_validation(self):
    for idx in self.rev_idx_range:
      rpi_pin_id_validator = pinid.RPiPinIdSet.validator(idx)
      for v in pinid.AllChipPinIdSet.valid_ids():
        if ( v not in pinid.RPiPinIdSet.valid_ids(idx)):
          self.assertFalse( rpi_pin_id_validator(v) )

  def test_invalid_pin_id_values_fail_validation(self):
    for idx in self.rev_idx_range:
      self.assertFalse( pinid.RPiPinIdSet.validator(idx)(-1) )
      self.assertFalse( pinid.RPiPinIdSet.validator(idx)("NaN") )
      self.assertFalse( pinid.RPiPinIdSet.validator(idx)(100000) )
      self.assertFalse( pinid.RPiPinIdSet.validator(idx)(None) )

  def test_in_range_p1_pin_values_return_valid_pin_id_or_none_from_p1_pin_to_gpio_pin_id(self):
    for idx in self.rev_idx_range:
      for p1_v in range(0,len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(idx))):
        id = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id(p1_v,idx)
        if ( id != None ):
          self.assertTrue( pinid.RPiPinIdSet.validator(idx)(id) )

  def test_bad_p1_pin_values_return_none_from_p1_pin_to_gpio_pin_id(self):
    for idx in self.rev_idx_range:
      self.assertIsNone( pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id(-1,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id(0,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id
                                                (
                                                  len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(idx))
                                                , idx
                                                )
                       )
      self.assertIsNone( pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id(None,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id("NaN",idx) )

  def test_in_range_p5_pin_values_return_valid_pin_id_or_none_from_p5_pin_to_gpio_pin_id(self):
    for idx in self.rev_idx_range:
      for p5_v in range(0,len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(idx))):
        id = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id(p5_v,idx)
        if ( id != None ):
          self.assertTrue( pinid.RPiPinIdSet.validator(idx)(id) )

  def test_bad_p5_pin_values_return_none_from_p5_pin_to_gpio_pin_id(self):
    for idx in self.rev_idx_range:
      self.assertIsNone( pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id(-1,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id(0,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id
                                                (
                                                  len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(idx))
                                                , idx
                                                )
                       )
      self.assertIsNone( pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id(None,idx) )
      self.assertIsNone( pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id("NaN",idx) )
                     
class TestPinIdValidator(object):
  def __init__(self, min, max):
    self.__min = min
    self.__max = max

  def __call__(self, value):
    try:
      value = int(value) # can we convert value to an int?
      if ( self.__min <= value and value <= self.__max ):
        return True
    except:
      pass
    return False

class PinIdRevisionUnitTestCases(unittest.TestCase):
  def test_0000_rpi_revision_accept_1_and_2_give_revision_indexes_0_and_1(self):
    pinid.PinId._set_rpi_gpio_revision(1)
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 0 )
    pinid.PinId._set_rpi_gpio_revision(2)
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 1 )
    pinid.PinId._set_rpi_gpio_revision(3)
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 2 )
    pinid.PinId._set_rpi_gpio_revision(4)
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 3 )

  def test_0020_rpi_revision_other_than_1_and_2_rasie_exception(self):
    with self.assertRaises( pinid.PinIdInvalidRevisionError ):
      pinid.PinId._set_rpi_gpio_revision(0)
    with self.assertRaises( pinid.PinIdInvalidRevisionError ):
      pinid.PinId._set_rpi_gpio_revision(5)
    with self.assertRaises( pinid.PinIdInvalidRevisionError ):
      pinid.PinId._set_rpi_gpio_revision(None)
    with self.assertRaises( pinid.PinIdInvalidRevisionError ):
      pinid.PinId._set_rpi_gpio_revision("crap")

class PinIdNonRevisionDependentUnitTestCases(unittest.TestCase):
  def setUp(self):
    pinid.PinId._set_rpi_gpio_revision(1)

  def test_0000_rpi_revision_index_setUp_to_be_zero(self):
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 0 )

  def test_create_from_test_all_ints_validator_OK(self):
    all_ints_validator = TestPinIdValidator(-sys.maxint - 1, sys.maxint)
    int_value = 3
    id = pinid.PinId(int_value, all_ints_validator)
    self.assertEqual( id, int_value )

  def test_create_from_test_all_ints_validator_BAD(self):
    zero_1_ints_validator = TestPinIdValidator(0,1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId(-1, zero_1_ints_validator)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId(2, zero_1_ints_validator)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId(None, zero_1_ints_validator)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId('Nan', zero_1_ints_validator)

  def test_create_good_chip_pin_id_using_any_chip_gpio_factory_method_ok(self):
    for v in pinid.AllChipPinIdSet.valid_ids():
      id = pinid.PinId.any_chip_gpio(v)
      self.assertEqual( id, v )

  def test_invalid_ids_to_any_chip_gpio_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.any_chip_gpio(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.any_chip_gpio("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.any_chip_gpio(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.any_chip_gpio(None)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.any_chip_gpio(len(pinid.AllChipPinIdSet.valid_ids()))

  def test_invalid_ids_to_gpio_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.gpio(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.gpio("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.gpio(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.gpio(None)

class PinIdRPiRev1UnitTestCases(unittest.TestCase):
  def setUp(self):
    pinid.PinId._set_rpi_gpio_revision(1)
    self.rev_idx = pinid.PinId._get_rpi_gpio_revision_index()

  def test_0000_rpi_revision_index_setUp_to_be_zero(self):
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 0 )
    self.assertEqual( self.rev_idx, 0 )

  def test_all_valid_chip_pin_ids_that_are_invalid_rpi_gpio_id_create_instance_fail(self):
    for v in pinid.AllChipPinIdSet.valid_ids():
      if ( v not in pinid.RPiPinIdSet.valid_ids(self.rev_idx)):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.gpio(v)

  def test_create_good_rpi_connector_pin_ids_using_gpio_factory_method_ok(self):
    for v in pinid.RPiPinIdSet.valid_ids(self.rev_idx):
      id = pinid.PinId.gpio(v)
      self.assertEqual( id, v )

  def test_valid_gpio_p1_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] != None ):
        id = pinid.PinId.p1_pin(i)
        self.assertEqual( id, p1_pin_to_gpio_id_map[i] )

  def test_invalid_gpio_p1_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] == None ):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(i)

  def test_invalid_p1_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(None)

  def test_no_p5_pin_numbers_are_valid(self): # no P5 for rev.1 boards
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      self.assertIsNone(p5_pin_to_gpio_id_map[i])               

  def test_invalid_gpio_p5_pin_numbers_raise_exception(self):
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      with self.assertRaises( pinid.PinIdInvalidError ):
        id = pinid.PinId.p5_pin(i)

  def test_invalid_p5_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(None)

# The following set of tests check the methods to create PinId instances
# representing specific Raspberry Pi P1 and P5 pins.
#
# To help weed out typos in the associated pin numbers and P1 pin to GPIO
# id mapping these values are repeated here, and used to cross check the
# resultant instances returned using these values. The values used here 
# were taken directly from the Raspberry Pi circuit diagram document.

  def test_p1_sda_valid(self):
    sda_p1_pin = 3
    gpio_id = 0
    sda_id = pinid.PinId.p1_sda()
    self.assertEqual( sda_id, pinid.PinId.p1_pin(sda_p1_pin) )
    self.assertEqual( sda_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_scl_valid(self):
    scl_p1_pin = 5
    gpio_id = 1
    scl_id = pinid.PinId.p1_scl()
    self.assertEqual( scl_id, pinid.PinId.p1_pin(scl_p1_pin) )
    self.assertEqual( scl_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gclk_valid(self):
    gpio_gclk_p1_pin = 7
    gpio_id = 4
    gpio_gclk_id = pinid.PinId.p1_gpio_gclk()
    self.assertEqual( gpio_gclk_id, pinid.PinId.p1_pin(gpio_gclk_p1_pin) )
    self.assertEqual( gpio_gclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_txd_valid(self):
    txd_p1_pin = 8
    gpio_id = 14
    txd_id = pinid.PinId.p1_txd()
    self.assertEqual( txd_id, pinid.PinId.p1_pin(txd_p1_pin) )
    self.assertEqual( txd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_rxd_valid(self):
    rxd_p1_pin = 10
    gpio_id = 15
    rxd_id = pinid.PinId.p1_rxd()
    self.assertEqual( rxd_id, pinid.PinId.p1_pin(rxd_p1_pin) )
    self.assertEqual( rxd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen0_valid(self):
    gpio_gen0_p1_pin = 11
    gpio_id = 17
    gpio_gen0_id = pinid.PinId.p1_gpio_gen0()
    self.assertEqual( gpio_gen0_id, pinid.PinId.p1_pin(gpio_gen0_p1_pin) )
    self.assertEqual( gpio_gen0_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen1_valid(self):
    gpio_gen1_p1_pin = 12
    gpio_id = 18
    gpio_gen1_id = pinid.PinId.p1_gpio_gen1()
    self.assertEqual( gpio_gen1_id, pinid.PinId.p1_pin(gpio_gen1_p1_pin) )
    self.assertEqual( gpio_gen1_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen2_valid(self):
    gpio_gen2_p1_pin = 13
    gpio_id = 21
    gpio_gen2_id = pinid.PinId.p1_gpio_gen2()
    self.assertEqual( gpio_gen2_id, pinid.PinId.p1_pin(gpio_gen2_p1_pin) )
    self.assertEqual( gpio_gen2_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen3_valid(self):
    gpio_gen3_p1_pin = 15
    gpio_id = 22
    gpio_gen3_id = pinid.PinId.p1_gpio_gen3()
    self.assertEqual( gpio_gen3_id, pinid.PinId.p1_pin(gpio_gen3_p1_pin) )
    self.assertEqual( gpio_gen3_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen4_valid(self):
    gpio_gen4_p1_pin = 16
    gpio_id = 23
    gpio_gen4_id = pinid.PinId.p1_gpio_gen4()
    self.assertEqual( gpio_gen4_id, pinid.PinId.p1_pin(gpio_gen4_p1_pin) )
    self.assertEqual( gpio_gen4_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen5_valid(self):
    gpio_gen5_p1_pin = 18
    gpio_id = 24
    gpio_gen5_id = pinid.PinId.p1_gpio_gen5()
    self.assertEqual( gpio_gen5_id, pinid.PinId.p1_pin(gpio_gen5_p1_pin) )
    self.assertEqual( gpio_gen5_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_mosi_valid(self):
    spi_mosi_p1_pin = 19
    gpio_id = 10
    spi_mosi_id = pinid.PinId.p1_spi_mosi()
    self.assertEqual( spi_mosi_id, pinid.PinId.p1_pin(spi_mosi_p1_pin) )
    self.assertEqual( spi_mosi_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_miso_valid(self):
    spi_miso_p1_pin = 21
    gpio_id = 9
    spi_miso_id = pinid.PinId.p1_spi_miso()
    self.assertEqual( spi_miso_id, pinid.PinId.p1_pin(spi_miso_p1_pin) )
    self.assertEqual( spi_miso_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen6_valid(self):
    gpio_gen6_p1_pin = 22
    gpio_id = 25
    gpio_gen6_id = pinid.PinId.p1_gpio_gen6()
    self.assertEqual( gpio_gen6_id, pinid.PinId.p1_pin(gpio_gen6_p1_pin) )
    self.assertEqual( gpio_gen6_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_sclk_valid(self):
    spi_sclk_p1_pin = 23
    gpio_id = 11
    spi_sclk_id = pinid.PinId.p1_spi_sclk()
    self.assertEqual( spi_sclk_id, pinid.PinId.p1_pin(spi_sclk_p1_pin) )
    self.assertEqual( spi_sclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce0_n_valid(self):
    spi_ce0_n_p1_pin = 24
    gpio_id = 8
    spi_ce0_n_id = pinid.PinId.p1_spi_ce0_n()
    self.assertEqual( spi_ce0_n_id, pinid.PinId.p1_pin(spi_ce0_n_p1_pin) )
    self.assertEqual( spi_ce0_n_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce1_n_valid(self):
    spi_ce1_n_p1_pin = 26
    gpio_id = 7
    spi_ce1_n_id = pinid.PinId.p1_spi_ce1_n()
    self.assertEqual( spi_ce1_n_id, pinid.PinId.p1_pin(spi_ce1_n_p1_pin) )
    self.assertEqual( spi_ce1_n_id, pinid.PinId.gpio(gpio_id) )

# The following tests check each of the P5 pin PinId creation functions.
# As P5 does not exist on revision 1 Raspberry Pi boards each of the P5
# pin PinId creation functions fail and raise a PinIdInvalidError exception.

  def test_p5_gpio_gen7_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen7()

  def test_p5_gpio_gen8_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen8()

  def test_p5_gpio_gen9_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen9()

  def test_p5_gpio_gen10_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen10()

class PinIdRPiRev2UnitTestCases(unittest.TestCase):
  def setUp(self):
    pinid.PinId._set_rpi_gpio_revision(2)
    self.rev_idx = pinid.PinId._get_rpi_gpio_revision_index()

  def test_0000_rpi_revision_index_setUp_to_be_one(self):
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 1 )
    self.assertEqual( self.rev_idx, 1 )

  def test_all_valid_chip_pin_ids_that_are_invalid_rpi_gpio_id_create_instance_fail(self):
    for v in pinid.AllChipPinIdSet.valid_ids():
      if ( v not in pinid.RPiPinIdSet.valid_ids(self.rev_idx)):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.gpio(v)

  def test_create_good_rpi_connector_pin_id_using_gpio_factory_method_ok(self):
    for v in pinid.RPiPinIdSet.valid_ids(self.rev_idx):
      id = pinid.PinId.gpio(v)
      self.assertEqual( id, v )

  def test_valid_gpio_p1_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] != None ):
        id = pinid.PinId.p1_pin(i)
        self.assertEqual( id, p1_pin_to_gpio_id_map[i] )

  def test_invalid_gpio_p1_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] == None ):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(i)

  def test_invalid_p1_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(None)

  def test_valid_gpio_p5_pin_numbers_create_instance_ok(self):
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      if ( p5_pin_to_gpio_id_map[i] != None ):
        id = pinid.PinId.p5_pin(i)
        self.assertEqual( id, p5_pin_to_gpio_id_map[i] )

  def test_invalid_gpio_p5_pin_numbers_raise_exception(self):
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      if ( p5_pin_to_gpio_id_map[i] == None ):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p5_pin(i)

  def test_invalid_p5_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(None)

# The following set of tests check the methods to create PinId instances
# representing specific Raspberry Pi P1 and P5 pins.
#
# To help weed out typos in the associated pin numbers and P1/P5 pin to GPIO
# id mapping these values are repeated here, and used to cross check the
# resultant instances returned using these values. The values used here 
# were taken directly from the Raspberry Pi circuit diagram document.

  def test_p1_sda_valid(self):
    sda_p1_pin = 3
    gpio_id = 2
    sda_id = pinid.PinId.p1_sda()
    self.assertEqual( sda_id, pinid.PinId.p1_pin(sda_p1_pin) )
    self.assertEqual( sda_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_scl_valid(self):
    scl_p1_pin = 5
    gpio_id = 3
    scl_id = pinid.PinId.p1_scl()
    self.assertEqual( scl_id, pinid.PinId.p1_pin(scl_p1_pin) )
    self.assertEqual( scl_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gclk_valid(self):
    gpio_gclk_p1_pin = 7
    gpio_id = 4
    gpio_gclk_id = pinid.PinId.p1_gpio_gclk()
    self.assertEqual( gpio_gclk_id, pinid.PinId.p1_pin(gpio_gclk_p1_pin) )
    self.assertEqual( gpio_gclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_txd_valid(self):
    txd_p1_pin = 8
    gpio_id = 14
    txd_id = pinid.PinId.p1_txd()
    self.assertEqual( txd_id, pinid.PinId.p1_pin(txd_p1_pin) )
    self.assertEqual( txd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_rxd_valid(self):
    rxd_p1_pin = 10
    gpio_id = 15
    rxd_id = pinid.PinId.p1_rxd()
    self.assertEqual( rxd_id, pinid.PinId.p1_pin(rxd_p1_pin) )
    self.assertEqual( rxd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen0_valid(self):
    gpio_gen0_p1_pin = 11
    gpio_id = 17
    gpio_gen0_id = pinid.PinId.p1_gpio_gen0()
    self.assertEqual( gpio_gen0_id, pinid.PinId.p1_pin(gpio_gen0_p1_pin) )
    self.assertEqual( gpio_gen0_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen1_valid(self):
    gpio_gen1_p1_pin = 12
    gpio_id = 18
    gpio_gen1_id = pinid.PinId.p1_gpio_gen1()
    self.assertEqual( gpio_gen1_id, pinid.PinId.p1_pin(gpio_gen1_p1_pin) )
    self.assertEqual( gpio_gen1_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen2_valid(self):
    gpio_gen2_p1_pin = 13
    gpio_id = 27
    gpio_gen2_id = pinid.PinId.p1_gpio_gen2()
    self.assertEqual( gpio_gen2_id, pinid.PinId.p1_pin(gpio_gen2_p1_pin) )
    self.assertEqual( gpio_gen2_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen3_valid(self):
    gpio_gen3_p1_pin = 15
    gpio_id = 22
    gpio_gen3_id = pinid.PinId.p1_gpio_gen3()
    self.assertEqual( gpio_gen3_id, pinid.PinId.p1_pin(gpio_gen3_p1_pin) )
    self.assertEqual( gpio_gen3_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen4_valid(self):
    gpio_gen4_p1_pin = 16
    gpio_id = 23
    gpio_gen4_id = pinid.PinId.p1_gpio_gen4()
    self.assertEqual( gpio_gen4_id, pinid.PinId.p1_pin(gpio_gen4_p1_pin) )
    self.assertEqual( gpio_gen4_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen5_valid(self):
    gpio_gen5_p1_pin = 18
    gpio_id = 24
    gpio_gen5_id = pinid.PinId.p1_gpio_gen5()
    self.assertEqual( gpio_gen5_id, pinid.PinId.p1_pin(gpio_gen5_p1_pin) )
    self.assertEqual( gpio_gen5_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_mosi_valid(self):
    spi_mosi_p1_pin = 19
    gpio_id = 10
    spi_mosi_id = pinid.PinId.p1_spi_mosi()
    self.assertEqual( spi_mosi_id, pinid.PinId.p1_pin(spi_mosi_p1_pin) )
    self.assertEqual( spi_mosi_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_miso_valid(self):
    spi_miso_p1_pin = 21
    gpio_id = 9
    spi_miso_id = pinid.PinId.p1_spi_miso()
    self.assertEqual( spi_miso_id, pinid.PinId.p1_pin(spi_miso_p1_pin) )
    self.assertEqual( spi_miso_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen6_valid(self):
    gpio_gen6_p1_pin = 22
    gpio_id = 25
    gpio_gen6_id = pinid.PinId.p1_gpio_gen6()
    self.assertEqual( gpio_gen6_id, pinid.PinId.p1_pin(gpio_gen6_p1_pin) )
    self.assertEqual( gpio_gen6_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_sclk_valid(self):
    spi_sclk_p1_pin = 23
    gpio_id = 11
    spi_sclk_id = pinid.PinId.p1_spi_sclk()
    self.assertEqual( spi_sclk_id, pinid.PinId.p1_pin(spi_sclk_p1_pin) )
    self.assertEqual( spi_sclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce0_n_valid(self):
    spi_ce0_n_p1_pin = 24
    gpio_id = 8
    spi_ce0_n_id = pinid.PinId.p1_spi_ce0_n()
    self.assertEqual( spi_ce0_n_id, pinid.PinId.p1_pin(spi_ce0_n_p1_pin) )
    self.assertEqual( spi_ce0_n_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce1_n_valid(self):
    spi_ce1_n_p1_pin = 26
    gpio_id = 7
    spi_ce1_n_id = pinid.PinId.p1_spi_ce1_n()
    self.assertEqual( spi_ce1_n_id, pinid.PinId.p1_pin(spi_ce1_n_p1_pin) )
    self.assertEqual( spi_ce1_n_id, pinid.PinId.gpio(gpio_id) )

  def test_p5_gpio_gen7_valid(self):
    gpio7_p5_pin = 3
    gpio_id = 28
    gpio_gen7_id = pinid.PinId.p5_gpio_gen7()
    self.assertEqual( gpio_gen7_id, pinid.PinId.p5_pin(gpio7_p5_pin) )
    self.assertEqual( gpio_gen7_id, pinid.PinId.gpio(gpio_id) )

  def test_p5_gpio_gen8_valid(self):
    gpio8_p5_pin = 4
    gpio_id = 29
    gpio_gen8_id = pinid.PinId.p5_gpio_gen8()
    self.assertEqual( gpio_gen8_id, pinid.PinId.p5_pin(gpio8_p5_pin) )
    self.assertEqual( gpio_gen8_id, pinid.PinId.gpio(gpio_id) )

  def test_p5_gpio_gen9_valid(self):
    gpio9_p5_pin = 5
    gpio_id = 30
    gpio_gen9_id = pinid.PinId.p5_gpio_gen9()
    self.assertEqual( gpio_gen9_id, pinid.PinId.p5_pin(gpio9_p5_pin) )
    self.assertEqual( gpio_gen9_id, pinid.PinId.gpio(gpio_id) )

  def test_p5_gpio_gen10_valid(self):
    gpio10_p5_pin = 6
    gpio_id = 31
    gpio_gen10_id = pinid.PinId.p5_gpio_gen10()
    self.assertEqual( gpio_gen10_id, pinid.PinId.p5_pin(gpio10_p5_pin) )
    self.assertEqual( gpio_gen10_id, pinid.PinId.gpio(gpio_id) )

class PinIdRPiRev3UnitTestCases(unittest.TestCase):
  def setUp(self):
    pinid.PinId._set_rpi_gpio_revision(3) # B+/A+, R'Pi 2.0
    self.rev_idx = pinid.PinId._get_rpi_gpio_revision_index()

  def test_0000_rpi_revision_index_setUp_to_be_two(self):
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 2 )
    self.assertEqual( self.rev_idx, 2 )

  def test_all_valid_chip_pin_ids_that_are_invalid_rpi_gpio_id_create_instance_fail(self):
    for v in pinid.AllChipPinIdSet.valid_ids():
      if ( v not in pinid.RPiPinIdSet.valid_ids(self.rev_idx)):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.gpio(v)

  def test_create_good_rpi_connector_pin_id_using_gpio_factory_method_ok(self):
    for v in pinid.RPiPinIdSet.valid_ids(self.rev_idx):
      id = pinid.PinId.gpio(v)
      self.assertEqual( id, v )

  def test_valid_gpio_j8_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] != None ):
        id = pinid.PinId.p1_pin(i)
        self.assertEqual( id, p1_pin_to_gpio_id_map[i] )

  def test_invalid_gpio_j8_pin_numbers_create_instance_ok(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      if ( p1_pin_to_gpio_id_map[i] == None ):
        with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(i)

  def test_invalid_j8_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p1_pin(None)

  def test_no_p5_pin_numbers_are_valid(self): # no P5 for B+/A+ & R'Pi 2.0 boards
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      self.assertIsNone(p5_pin_to_gpio_id_map[i])               

  def test_invalid_gpio_p5_pin_numbers_raise_exception(self):
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      with self.assertRaises( pinid.PinIdInvalidError ):
        id = pinid.PinId.p5_pin(i)

  def test_invalid_p5_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(None)

# The following set of tests check the methods to create PinId instances
# representing specific Raspberry Pi P1/J8 and P5 pins.
#
# To help weed out typos in the associated pin numbers and P1/P5 pin to GPIO
# id mapping these values are repeated here, and used to cross check the
# resultant instances returned using these values. The values used here 
# were taken directly from the Raspberry Pi circuit diagram document.

  def test_p1_sda_valid(self):
    sda_p1_pin = 3
    gpio_id = 2
    sda_id = pinid.PinId.p1_sda()
    self.assertEqual( sda_id, pinid.PinId.p1_pin(sda_p1_pin) )
    self.assertEqual( sda_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_scl_valid(self):
    scl_p1_pin = 5
    gpio_id = 3
    scl_id = pinid.PinId.p1_scl()
    self.assertEqual( scl_id, pinid.PinId.p1_pin(scl_p1_pin) )
    self.assertEqual( scl_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gclk_valid(self):
    gpio_gclk_p1_pin = 7
    gpio_id = 4
    gpio_gclk_id = pinid.PinId.p1_gpio_gclk()
    self.assertEqual( gpio_gclk_id, pinid.PinId.p1_pin(gpio_gclk_p1_pin) )
    self.assertEqual( gpio_gclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_txd_valid(self):
    txd_p1_pin = 8
    gpio_id = 14
    txd_id = pinid.PinId.p1_txd()
    self.assertEqual( txd_id, pinid.PinId.p1_pin(txd_p1_pin) )
    self.assertEqual( txd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_rxd_valid(self):
    rxd_p1_pin = 10
    gpio_id = 15
    rxd_id = pinid.PinId.p1_rxd()
    self.assertEqual( rxd_id, pinid.PinId.p1_pin(rxd_p1_pin) )
    self.assertEqual( rxd_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen0_valid(self):
    gpio_gen0_p1_pin = 11
    gpio_id = 17
    gpio_gen0_id = pinid.PinId.p1_gpio_gen0()
    self.assertEqual( gpio_gen0_id, pinid.PinId.p1_pin(gpio_gen0_p1_pin) )
    self.assertEqual( gpio_gen0_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen1_valid(self):
    gpio_gen1_p1_pin = 12
    gpio_id = 18
    gpio_gen1_id = pinid.PinId.p1_gpio_gen1()
    self.assertEqual( gpio_gen1_id, pinid.PinId.p1_pin(gpio_gen1_p1_pin) )
    self.assertEqual( gpio_gen1_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen2_valid(self):
    gpio_gen2_p1_pin = 13
    gpio_id = 27
    gpio_gen2_id = pinid.PinId.p1_gpio_gen2()
    self.assertEqual( gpio_gen2_id, pinid.PinId.p1_pin(gpio_gen2_p1_pin) )
    self.assertEqual( gpio_gen2_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen3_valid(self):
    gpio_gen3_p1_pin = 15
    gpio_id = 22
    gpio_gen3_id = pinid.PinId.p1_gpio_gen3()
    self.assertEqual( gpio_gen3_id, pinid.PinId.p1_pin(gpio_gen3_p1_pin) )
    self.assertEqual( gpio_gen3_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen4_valid(self):
    gpio_gen4_p1_pin = 16
    gpio_id = 23
    gpio_gen4_id = pinid.PinId.p1_gpio_gen4()
    self.assertEqual( gpio_gen4_id, pinid.PinId.p1_pin(gpio_gen4_p1_pin) )
    self.assertEqual( gpio_gen4_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen5_valid(self):
    gpio_gen5_p1_pin = 18
    gpio_id = 24
    gpio_gen5_id = pinid.PinId.p1_gpio_gen5()
    self.assertEqual( gpio_gen5_id, pinid.PinId.p1_pin(gpio_gen5_p1_pin) )
    self.assertEqual( gpio_gen5_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_mosi_valid(self):
    spi_mosi_p1_pin = 19
    gpio_id = 10
    spi_mosi_id = pinid.PinId.p1_spi_mosi()
    self.assertEqual( spi_mosi_id, pinid.PinId.p1_pin(spi_mosi_p1_pin) )
    self.assertEqual( spi_mosi_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_miso_valid(self):
    spi_miso_p1_pin = 21
    gpio_id = 9
    spi_miso_id = pinid.PinId.p1_spi_miso()
    self.assertEqual( spi_miso_id, pinid.PinId.p1_pin(spi_miso_p1_pin) )
    self.assertEqual( spi_miso_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_gpio_gen6_valid(self):
    gpio_gen6_p1_pin = 22
    gpio_id = 25
    gpio_gen6_id = pinid.PinId.p1_gpio_gen6()
    self.assertEqual( gpio_gen6_id, pinid.PinId.p1_pin(gpio_gen6_p1_pin) )
    self.assertEqual( gpio_gen6_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_sclk_valid(self):
    spi_sclk_p1_pin = 23
    gpio_id = 11
    spi_sclk_id = pinid.PinId.p1_spi_sclk()
    self.assertEqual( spi_sclk_id, pinid.PinId.p1_pin(spi_sclk_p1_pin) )
    self.assertEqual( spi_sclk_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce0_n_valid(self):
    spi_ce0_n_p1_pin = 24
    gpio_id = 8
    spi_ce0_n_id = pinid.PinId.p1_spi_ce0_n()
    self.assertEqual( spi_ce0_n_id, pinid.PinId.p1_pin(spi_ce0_n_p1_pin) )
    self.assertEqual( spi_ce0_n_id, pinid.PinId.gpio(gpio_id) )

  def test_p1_spi_ce1_n_valid(self):
    spi_ce1_n_p1_pin = 26
    gpio_id = 7
    spi_ce1_n_id = pinid.PinId.p1_spi_ce1_n()
    self.assertEqual( spi_ce1_n_id, pinid.PinId.p1_pin(spi_ce1_n_p1_pin) )
    self.assertEqual( spi_ce1_n_id, pinid.PinId.gpio(gpio_id) )

# The following tests check each of the P5 pin PinId creation functions.
# As P5 does not exist on A+/B+ & Raspberry Pi 2.0 boards each of the P5
# pin PinId creation functions fail and raise a PinIdInvalidError exception.

  def test_p5_gpio_gen7_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen7()

  def test_p5_gpio_gen8_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen8()

  def test_p5_gpio_gen9_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen9()

  def test_p5_gpio_gen10_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen10()


class PinIdRPiRev4UnitTestCases(unittest.TestCase):
  def setUp(self):
    pinid.PinId._set_rpi_gpio_revision(4) # compute module
    self.rev_idx = pinid.PinId._get_rpi_gpio_revision_index()

  def test_0000_rpi_revision_index_setUp_to_be_three(self):
    self.assertEqual( pinid.PinId._get_rpi_gpio_revision_index(), 3 )
    self.assertEqual( self.rev_idx, 3 )

  def test_all_valid_chip_pin_ids_that_are_invalid_rpi_gpio_id_create_instance_fail(self):
      for v in pinid.AllChipPinIdSet.valid_ids():
          if ( v not in pinid.RPiPinIdSet.valid_ids(self.rev_idx)):
              with self.assertRaises( pinid.PinIdInvalidError ):
                  id = pinid.PinId.gpio(v)

  def test_no_p1_pin_numbers_are_valid(self): # no P1/J8 for compute modules
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      self.assertIsNone(p1_pin_to_gpio_id_map[i])               

  def test_invalid_gpio_p1_pin_numbers_raise_exception(self):
    p1_pin_to_gpio_id_map = pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p1_pin_to_gpio_id_map) ):
      with self.assertRaises( pinid.PinIdInvalidError ):
        id = pinid.PinId.p1_pin(i)

  def test_invalid_j8_pin_numbers_cause_instance_creation_fail(self):
      with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(-1)
      with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin("NaN")
      with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(100000)
      with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(len(pinid.RPiPinIdSet.p1_pin_to_gpio_pin_id_tuple(self.rev_idx)))
      with self.assertRaises( pinid.PinIdInvalidError ):
          id = pinid.PinId.p1_pin(None)

  def test_no_p5_pin_numbers_are_valid(self): # no P5 for B+/A+ & R'Pi 2.0 boards
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      self.assertIsNone(p5_pin_to_gpio_id_map[i])               

  def test_invalid_gpio_p5_pin_numbers_raise_exception(self):
    p5_pin_to_gpio_id_map = pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx);
    for i in range( 0, len(p5_pin_to_gpio_id_map) ):
      with self.assertRaises( pinid.PinIdInvalidError ):
        id = pinid.PinId.p5_pin(i)

  def test_invalid_p5_pin_numbers_cause_instance_creation_fail(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(-1)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin("NaN")
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(100000)
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(len(pinid.RPiPinIdSet.p5_pin_to_gpio_pin_id_tuple(self.rev_idx)))
    with self.assertRaises( pinid.PinIdInvalidError ):
      id = pinid.PinId.p5_pin(None)

# The following set of tests check the methods to create PinId instances
# representing specific Raspberry Pi P1/J8 and P5 pins.
#
# As the compute module has no header pins - either P1/J8 or P5 - each of the
# P1/J8 and P5 pin PinId creation functions fail and raise a PinIdInvalidError
# exception.

  def test_p1_sda_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_sda()

  def test_p1_scl_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_scl()

  def test_p1_gpio_gclk_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gclk()

  def test_p1_txd_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_txd()

  def test_p1_rxd_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_rxd()

  def test_p1_gpio_gen0_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen0()

  def test_p1_gpio_gen1_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen1()

  def test_p1_gpio_gen2_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen2()

  def test_p1_gpio_gen3_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen3()

  def test_p1_gpio_gen4_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen4()

  def test_p1_gpio_gen5_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen5()

  def test_p1_spi_mosi_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_spi_mosi()

  def test_p1_spi_miso_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_spi_miso()

  def test_p1_gpio_gen6_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_gpio_gen6()

  def test_p1_spi_sclk_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_spi_sclk()

  def test_p1_spi_ce0_n_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_spi_ce0_n()

  def test_p1_spi_ce1_n_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p1_spi_ce1_n()

  def test_p5_gpio_gen7_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen7()

  def test_p5_gpio_gen8_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen8()

  def test_p5_gpio_gen9_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen9()

  def test_p5_gpio_gen10_invalid(self):
    with self.assertRaises( pinid.PinIdInvalidError ):
      pinid.PinId.p5_gpio_gen10()

if __name__ == '__main__':
  unittest.main()
