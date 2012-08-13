'''
    Part of the dibase.rpi.gpio.test package.

    System tests on read/write operations on GPIO pin groupos
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
from gpio import pingroup
from gpio import pin
from gpio import pinid
from gpio import gpioerror as error

class OpenPinGroupFunctionSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_open_pins_for_writing_bad_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'w#I')

    def test_open_pins_for_writing_bad_format_mode_fails(self):
        with self.assertRaises( error.PinGroupFormatModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wN#')

    def test_open_pins_for_writing_bad_blocking_or_format_mode_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'w#')

    def test_open_pin_for_writing_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'w'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_nonblocking_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'wN'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_integer_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'wI'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_noblocking_integer_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'wNI'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_sequence_mode_creates_PinListWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'wS'),pingroup.PinListWriter)

    def test_open_pin_for_writing_nonblocking_sequence_mode_creates_PinListWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pin.PinId.p1_gpio_gen0()],'wNS'),pingroup.PinListWriter)

    def test_open_pins_for_writing_some_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wRI')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wFS')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wBI')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wR')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wF')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'wB')

    def test_open_pins_for_reading_bad_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rXS')

    def test_open_pins_for_reading_bad_format_mode_fails(self):
        with self.assertRaises( error.PinGroupFormatModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rBX')

    def test_open_pins_for_reading_bad_blocking_or_format_mode_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'r#')

    def test_open_pins_bad_rw_mode_fails(self):
        with self.assertRaises( error.PinDirectionModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'a')

    def test_open_pins_bad_mode_string_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rNS+')

    def test_open_pin_for_reading_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'r'),pingroup.PinWordReader)

    def test_open_pin_for_reading_nonblocking_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rN'),pingroup.PinWordReader)

    def test_open_pin_for_reading_integer_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rI'),pingroup.PinWordReader)

    def test_open_pin_for_reading_nonblocking_integer_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rNI'),pingroup.PinWordReader)

    def test_open_pin_default_mode_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0()),pingroup.PinWordReader)

    def test_open_pin_empty_mode_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),''),pingroup.PinWordReader)

    def test_open_pin_for_reading_sequence_mode_creates_creates_PinListReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rS'),pingroup.PinListReader)

    def test_open_pin_for_reading_nonblocking_sequence_mode_creates_creates_PinListReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rNS'),pingroup.PinListReader)

    def test_open_pin_for_reading_blockonfallingedge_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rF'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rR'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rB'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonfallingedge_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rFI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rRI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rBI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonfallingedge_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rFS'),pingroup.PinListBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rRS'),pingroup.PinListBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup(pin.PinId.p1_gpio_gen0(),'rBS'),pingroup.PinListBlockingReader)

class PinWordWriterSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordWriter(23)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordWriter(None)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordWriter(1.234)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordWriter(False)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordWriter([])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordWriter([-1])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordWriter(["Nan"])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordWriter("Nan") # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordWriter([100000])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordWriter([None])

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinWordWriter([4,23,23])
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinWordWriter([23,4])

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        a_pin_group.close()
        a_pin_group = pingroup.PinWordWriter([23,4,7])

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_cloed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinWordWriter([23,4,7]) as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinWordWriter([23,4,7])
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_write_non_scalar_value_raises_TypeError(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        with self.assertRaises( TypeError ):
            a_pin_group.write(["Nan"])
        with self.assertRaises( TypeError ):
            a_pin_group.write([1,0,1])
        with self.assertRaises( TypeError ):
            a_pin_group.write([True, False, True])
        a_pin_group.close()

    def test_write_scalar_value_not_convertible_to_integer_raises_ValueError(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        with self.assertRaises( ValueError ):
            a_pin_group.write("Nan")
        a_pin_group.close()

    def test_write_out_of_range_value_raises_ValueError(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        with self.assertRaises( ValueError ):
            a_pin_group.write(-1)
        with self.assertRaises( ValueError ):
            a_pin_group.write(8)
        a_pin_group.close()

class XPinGroupIOSystemTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in pinid.RPiPinIdSet.valid_ids():
            id = pin.force_free_pin(pin.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_00100_write_0_to_7_and_down_again_to_gen_gpio0_to_2(self):
        a_pin_group = pingroup.open_pingroup( [ pin.PinId.p1_gpio_gen0()\
                                              , pin.PinId.p1_gpio_gen1()\
                                              , pin.PinId.p1_gpio_gen2()\
                                              ]\
                                            , 'w')
        for i in range(8):
            time.sleep(0.5)
            a_pin_group.write(i)
        for i in range(7,-1,-1):
            time.sleep(0.5)
            a_pin_group.write(i)

    def test_00150_time_writes_0_to_15_on_gen_gpio0_to_3(self):
        a_pin_group = pingroup.open_pingroup( [ pin.PinId.p1_gpio_gen0()\
                                              , pin.PinId.p1_gpio_gen1()\
                                              , pin.PinId.p1_gpio_gen2()\
                                              , pin.PinId.p1_gpio_gen3()\
                                              ]\
                                            , 'w')
        ITERATIONS = 200
        print "\nStarting pin group write timing..."
        time.sleep(0.05)
        then = time.time()
        for it in range(ITERATIONS):
            for i in range(16):
                a_pin_group.write(i)
        now = time.time()
        a_pin_group.write(0)
        print ITERATIONS, "* 0..15 GPIO pin group writes took:", now - then, "seconds."

if __name__ == '__main__':
    unittest.main()
