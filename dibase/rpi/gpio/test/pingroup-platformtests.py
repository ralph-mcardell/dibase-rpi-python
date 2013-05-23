'''
    Part of the dibase.rpi.gpio.test package.

    Platform tests on read/write operations on GPIO pin group
    IO type instances.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

import collections
import time
import unittest
import sys
if __name__ == '__main__':
# Add path to directory containing the dibase package directory
    sys.path.insert(0, './../../../..') 
from dibase.rpi.gpio import pingroup
from dibase.rpi.gpio.pin import force_free_pin
from dibase.rpi.gpio.pinid import RPiPinIdSet
from dibase.rpi.gpio import gpioerror as error

class OpenPinGroupFunctionPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_open_pins_for_writing_bad_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'w#I')

    def test_open_pins_for_writing_bad_format_mode_fails(self):
        with self.assertRaises( error.PinGroupFormatModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wN#')

    def test_open_pins_for_writing_bad_blocking_or_format_mode_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'w#')

    def test_open_pin_for_writing_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'w'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_nonblocking_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wN'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_integer_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wI'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_noblocking_integer_mode_creates_PinWordWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wNI'),pingroup.PinWordWriter)

    def test_open_pin_for_writing_sequence_mode_creates_PinListWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wS'),pingroup.PinListWriter)

    def test_open_pin_for_writing_nonblocking_sequence_mode_creates_PinListWriter(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wNS'),pingroup.PinListWriter)

    def test_open_pins_for_writing_some_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wRI')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wFS')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wBI')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wR')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wF')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'wB')

    def test_open_pins_for_reading_bad_blocking_mode_fails(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rXS')

    def test_open_pins_for_reading_bad_format_mode_fails(self):
        with self.assertRaises( error.PinGroupFormatModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rBX')

    def test_open_pins_for_reading_bad_blocking_or_format_mode_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'r#')

    def test_open_pins_bad_rw_mode_fails(self):
        with self.assertRaises( error.PinDirectionModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'a')

    def test_open_pins_bad_mode_string_fails(self):
        with self.assertRaises( error.PinGroupOpenModeInvalidError ):
            pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rNS+')

    def test_open_pin_for_reading_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'r'),pingroup.PinWordReader)

    def test_open_pin_for_reading_nonblocking_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rN'),pingroup.PinWordReader)

    def test_open_pin_for_reading_integer_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rI'),pingroup.PinWordReader)

    def test_open_pin_for_reading_nonblocking_integer_mode_creates_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rNI'),pingroup.PinWordReader)

    def test_open_pin_default_mode_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()]),pingroup.PinWordReader)

    def test_open_pin_empty_mode_creates_PinWordReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],''),pingroup.PinWordReader)

    def test_open_pin_for_reading_sequence_mode_creates_creates_PinListReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rS'),pingroup.PinListReader)

    def test_open_pin_for_reading_nonblocking_sequence_mode_creates_creates_PinListReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rNS'),pingroup.PinListReader)

    def test_open_pin_for_reading_blockonfallingedge_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rF'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rR'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rB'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonfallingedge_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rFI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rRI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_integer_mode_creates_PinWordBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rBI'),pingroup.PinWordBlockingReader)

    def test_open_pin_for_reading_blockonfallingedge_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rFS'),pingroup.PinListBlockingReader)

    def test_open_pin_for_reading_blockonrisingedge_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rRS'),pingroup.PinListBlockingReader)

    def test_open_pin_for_reading_blockonbothedges_sequence_mode_creates_PinListBlockingReader(self):
        self.assertIsInstance(pingroup.open_pingroup([pingroup.PinId.p1_gpio_gen0()],'rBS'),pingroup.PinListBlockingReader)

class PinWordReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordReader(23)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordReader(None)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordReader(1.234)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordReader(False)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordReader([])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordReader([-1])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordReader(["Nan"])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordReader("Nan") # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordReader([100000])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordReader([None])

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinWordReader([4,23,23])
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinWordReader([23,4])

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        a_pin_group.close()
        a_pin_group = pingroup.PinWordReader([23,4,7])

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_closed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinWordReader([23,4,7]) as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinWordReader([23,4,7])
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.read()

    def test_read_returns_integer_type(self):
        a_pin_group = pingroup.PinWordReader([23,4,7])
        self.assertIsInstance(a_pin_group.read(), (int,long))
        a_pin_group.close()

class PinListReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListReader(23)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListReader(None)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListReader(1.234)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListReader(False)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListReader([])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListReader([-1])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListReader(["Nan"])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListReader("Nan") # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListReader([100000])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListReader([None])

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinListReader([4,23,23])
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinListReader([23,4])

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        a_pin_group.close()
        a_pin_group = pingroup.PinListReader([23,4,7])

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_closed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinListReader([23,4,7]) as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinListReader([23,4,7])
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.read()

    def test_read_returns_iterable_type(self):
        a_pin_group = pingroup.PinListReader([23,4,7])
        self.assertIsInstance(a_pin_group.read(), collections.Iterable)
        a_pin_group.close()

class PinWordBlockingReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader(23,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader(None,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader(1.234,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader(False,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([],'B')

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([-1],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader(["Nan"],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader("Nan",'B') # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([100000],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([None],'B')

    def test_invalid_blocking_mode_fail_pin_creation(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([7],'N')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            a_pin_group = pingroup.PinWordBlockingReader([7],'X')
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinWordBlockingReader([7],23)
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinWordBlockingReader([7],[5])
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinWordBlockingReader([7],None)

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinWordBlockingReader([4,23,23],'B')
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinWordBlockingReader([23,4],'B')

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_closed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinWordBlockingReader([23,4,7],'B') as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinWordBlockingReader([23,4,7],'B')
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.read(0)

    def test_polled_read_returns_integer_type(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        self.assertIsInstance(a_pin_group.read(0), (int,long))
        a_pin_group.close()

    def test_timeout_read_returns_None(self):
        a_pin_group = pingroup.PinWordBlockingReader([23,4,7],'B')
        a_pin_group.read(0) # reset initial signalled states
        self.assertIsNone(a_pin_group.read(0.001))
        a_pin_group.close()


class PinListBlockingReaderPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader(23,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader(None,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader(1.234,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader(False,'B')
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([],'B')

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([-1],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader(["Nan"],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader("Nan",'B') # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([100000],'B')
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([None],'B')

    def test_invalid_blocking_mode_fail_pin_creation(self):
        with self.assertRaises( error.PinBlockModeInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([7],'N')
        with self.assertRaises( error.PinBlockModeInvalidError ):
            a_pin_group = pingroup.PinListBlockingReader([7],'X')
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinListBlockingReader([7],23)
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinListBlockingReader([7],[5])
        with self.assertRaises( TypeError ):
            a_pin_group = pingroup.PinListBlockingReader([7],None)

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinListBlockingReader([4,23,23],'B')
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinListBlockingReader([23,4],'B')

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_closed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinListBlockingReader([23,4,7],'B') as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinListBlockingReader([23,4,7],'B')
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.read(0)

    def test_polled_read_returns_iterable_type(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        self.assertIsInstance(a_pin_group.read(0), collections.Iterable)
        a_pin_group.close()

    def test_timeout_read_returns_None(self):
        a_pin_group = pingroup.PinListBlockingReader([23,4,7],'B')
        a_pin_group.read(0) # reset initial signalled states
        self.assertIsNone(a_pin_group.read(0.001))
        a_pin_group.close()

class PinWordWriterPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
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
 
    def test_pin_group_closed_on_with_exit(self):
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

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinWordWriter([23,4,7])
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.write(0)

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

class PinListWriterPlatformTests(unittest.TestCase):
    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_invalid_pin_ids_sequence_fail_pin_creation(self):
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListWriter(23)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListWriter(None)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListWriter(1.234)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListWriter(False)
        with self.assertRaises( error.PinGroupIdsInvalidError ):
            a_pin_group = pingroup.PinListWriter([])

    def test_invalid_pin_ids_fail_pin_creation(self):
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListWriter([-1])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListWriter(["Nan"])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListWriter("Nan") # strings are iterable sequences!
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListWriter([100000])
        with self.assertRaises( error.PinIdInvalidError ):
            a_pin_group = pingroup.PinListWriter([None])

    def test_already_used_pin_id_fails_pin_creation_and_closes_any_open_pins(self):
        with self.assertRaises( error.PinInUseError ):
            a_pin_group = pingroup.PinListWriter([4,23,23])
        # try to open pins 4 & 23 again - if they were not closed when
        # above group create failed then PinInUseError will be thrown.
        a_pin_group = pingroup.PinListWriter([23,4])

    def test_close_closes_all_opened_pins(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group.close()
        a_pin_group = pingroup.PinListWriter([23,4,7])

    def test_closed_reports_pin_group_state(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        self.assertFalse(a_pin_group.closed())
        a_pin_group.close()
        self.assertTrue(a_pin_group.closed())

    def test_multiple_close_calls_do_nothing_bad(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group.close()
        a_pin_group.close()
        a_pin_group.close()        
        self.assertTrue(a_pin_group.closed())
 
    def test_pin_group_closed_on_with_exit(self):
        outside_pg = None
        with pingroup.PinListWriter([23,4,7]) as pg:
            outside_pg = pg
            self.assertFalse(pg.closed())
            self.assertFalse(outside_pg.closed())
        self.assertTrue(outside_pg.closed())
        pingroup.PinListWriter([23,4,7])
 
    def test_file_descriptors_returns_expected_number_and_type_of_descriptors(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertEqual(len(a_pin_group_fds), 3)
        for fd in a_pin_group_fds:
            self.assertIsInstance(fd, int)

    def test_file_descriptors_returns_empty_list_if_pin_group_closed(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group.close()
        a_pin_group_fds = a_pin_group.file_descriptors()
        self.assertFalse(a_pin_group_fds)

    def test_read_closed_group_raises_ValueError(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group.close()
        with self.assertRaises( ValueError ):
            a_pin_group.write([0,0,0])

    def test_write_non_iterable_value_raises_TypeError(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        with self.assertRaises( TypeError ):
            a_pin_group.write(1)
        with self.assertRaises( TypeError ):
            a_pin_group.write(False)
        with self.assertRaises( TypeError ):
            a_pin_group.write(None)
        with self.assertRaises( TypeError ):
            a_pin_group.write(set([True, False, True]))
        a_pin_group.close()

    def test_write_iterable_wrong_number_of_elements_raises_TypeError(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        with self.assertRaises( TypeError ):
            a_pin_group.write([])
        with self.assertRaises( TypeError ):
            a_pin_group.write([1])
        with self.assertRaises( TypeError ):
            a_pin_group.write([1,2])
        with self.assertRaises( TypeError ):
            a_pin_group.write([1,2,3,4])
        a_pin_group.close()

    def test_write_iterable_right_number_of_elements_raises_nothing(self):
        a_pin_group = pingroup.PinListWriter([23,4,7])
        a_pin_group.write([False,0,[]])
        a_pin_group.close()

if __name__ == '__main__':
    unittest.main()
