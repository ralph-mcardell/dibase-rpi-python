'''
    Part of the dibase.rpi.gpio.test package.

    Interactive platform tests on read/write operations on GPIO pin group
    IO type instances.

    Tests require either observation or GPIO input line state modification
    that probably implies user interaction.               |

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

# Interactive test setup:
# Connect: 
# P1 pin 11 - GPIO_GEN0 - 
# P1 pin 12 - GPIO_GEN1  | to output indicators such as an LEDs
# P1 pin 13 - GPIO_GEN2  |
# P1 pin 15 - GPIO_GEN3 - 
#
# P1 pin 22 - GPIO_GEN6 \ to an input devices such as a switches that can
# P1 pin 7  - GPIO_GCLK / toggle between low and high states.

class PinGroupInteractivePlatformTests(unittest.TestCase):
    __skip = False

    @classmethod
    def setUpClass(cls):
      print "To run these tests please connect the following GPIO pins:"
      print "P1 pin 11 - GPIO_GEN0 -"
      print "P1 pin 12 - GPIO_GEN1  | to output indicators such as an LEDs."
      print "P1 pin 13 - GPIO_GEN2  |"
      print "P1 pin 15 - GPIO_GEN3 - "
      print ""
      print "P1 pin 22 - GPIO_GEN6 \ to an input devices such as a switches that"
      print "P1 pin 7  - GPIO_GCLK / can toggle between low and high states."
      option = raw_input("Press enter when ready or Q to quit...")
      if option=='Q' or option=='q':
        PinGroupInteractivePlatformTests.__skip = True

    def setUp(self):
      if PinGroupInteractivePlatformTests.__skip:
        self.skipTest('User quit request')

    def tearDown(self):
        cleaned_up = []
        for v in RPiPinIdSet.valid_ids(pingroup.PinId._get_rpi_major_revision_index()):
            id = force_free_pin(pingroup.PinId.gpio(v))
            if (id!=None):
                cleaned_up.append(id)
        if ( cleaned_up != [] ):
            print "\nCleaned up left over exports for pins", cleaned_up
        self.assertEqual(cleaned_up,[])

    def test_00100_write_0_to_7_and_down_again_to_gen_gpio0_to_2(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()\
                                              , pingroup.PinId.p1_gpio_gen1()\
                                              , pingroup.PinId.p1_gpio_gen2()\
                                              ]\
                                            , 'w')
        self.assertIsInstance(a_pin_group,pingroup.PinWordWriter)
        for i in range(8):
            time.sleep(0.5)
            a_pin_group.write(i)
        for i in range(7,-1,-1):
            time.sleep(0.5)
            a_pin_group.write(i)

    def test_00150_time_writes_0_to_15_on_gen_gpio0_to_3(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()\
                                              , pingroup.PinId.p1_gpio_gen1()\
                                              , pingroup.PinId.p1_gpio_gen2()\
                                              , pingroup.PinId.p1_gpio_gen3()\
                                              ]\
                                            , 'w')
        self.assertIsInstance(a_pin_group,pingroup.PinWordWriter)
        ITERATIONS = 200
        print "\nStarting pin group word write timing..."
        time.sleep(0.05)
        then = time.time()
        for it in range(ITERATIONS):
            for i in range(16):
                a_pin_group.write(i)
        now = time.time()
        a_pin_group.write(0)
        print ITERATIONS, "* 0..15 GPIO pin group writes took:", now - then, "seconds."

    def test_01100_write_F_F_F_to_T_T_T_and_down_again_to_gen_gpio0_to_2(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()\
                                              , pingroup.PinId.p1_gpio_gen1()\
                                              , pingroup.PinId.p1_gpio_gen2()\
                                              ]\
                                            , 'wS')
        self.assertIsInstance(a_pin_group,pingroup.PinListWriter)
        states =    [   [False, False, False]\
                    ,   [ True, False, False]\
                    ,   [False,  True, False]\
                    ,   [ True,  True, False]\
                    ,   [False, False,  True]\
                    ,   [ True, False,  True]\
                    ,   [False,  True,  True]\
                    ,   [ True,  True,  True]\
                    ]
        for i in states:
            time.sleep(0.5)
            a_pin_group.write(i)
        for i in reversed(states):
            time.sleep(0.5)
            a_pin_group.write(i)

    def test_01150_time_writes_F_F_F_F_to_T_T_T_T_on_gen_gpio0_to_3(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen0()\
                                              , pingroup.PinId.p1_gpio_gen1()\
                                              , pingroup.PinId.p1_gpio_gen2()\
                                              , pingroup.PinId.p1_gpio_gen3()\
                                              ]\
                                            , 'wS')
        self.assertIsInstance(a_pin_group,pingroup.PinListWriter)
        states =    [   [False, False, False, False]\
                    ,   [ True, False, False, False]\
                    ,   [False,  True, False, False]\
                    ,   [ True,  True, False, False]\
                    ,   [False, False,  True, False]\
                    ,   [ True, False,  True, False]\
                    ,   [False,  True,  True, False]\
                    ,   [ True,  True,  True, False]\
                    ,   [False, False, False,  True]\
                    ,   [ True, False, False,  True]\
                    ,   [False,  True, False,  True]\
                    ,   [ True,  True, False,  True]\
                    ,   [False, False,  True,  True]\
                    ,   [ True, False,  True,  True]\
                    ,   [False,  True,  True,  True]\
                    ,   [ True,  True,  True,  True]\
                    ]
        ITERATIONS = 200
        print "\nStarting pin group sequence write timing..."
        time.sleep(0.05)
        then = time.time()
        for it in range(ITERATIONS):
            for i in states:
                a_pin_group.write(i)
        now = time.time()
        a_pin_group.write(states[0])
        print ITERATIONS, "* F,F,F,F..T,T,T,T GPIO pin group writes took:", now - then, "seconds."

    def test_02100_read_word_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'r')
        self.assertIsInstance(a_pin_group,pingroup.PinWordReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 0)
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 1)
        print "Make P1 pin GPIO_GEN6  LOW  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 2)
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 3)

    def test_03100_read_sequence_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rS')
        self.assertIsInstance(a_pin_group,pingroup.PinListReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [False,False])
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [True,False])
        print "Make P1 pin GPIO_GEN6  LOW  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [False,True])
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [True,True])

    def test_04100_poll_blocking_read_word_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rB')
        self.assertIsInstance(a_pin_group,pingroup.PinWordBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), 0)
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), 1)
        print "Make P1 pin GPIO_GEN6  LOW  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), 2)
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), 3)

    def test_04150_blocking_both_read_word_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rB')
        self.assertIsInstance(a_pin_group,pingroup.PinWordBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 0)
        print "Change P1 pin GPIO_GEN6 to HIGH  keep   GPIO_GCLK at  LOW..."
        self.assertEquals(a_pin_group.read(), 1)
        print "Keep   P1 pin GPIO_GEN6 at HIGH  change GPIO_GCLK to HIGH..."
        self.assertEquals(a_pin_group.read(), 3)
        print "Change P1 pin GPIO_GEN6 to  LOW  keep   GPIO_GCLK at HIGH..."

        self.assertEquals(a_pin_group.read(), 2)

    def test_04200_blocking_rising_read_word_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rR')
        self.assertIsInstance(a_pin_group,pingroup.PinWordBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), 0)
        print "Toggle P1 pin GPIO_GEN6 state keep   GPIO_GCLK   LOW..."
        self.assertEquals(a_pin_group.read(), 1)
        print "Keep   P1 pin GPIO_GEN6  LOW  toggle GPIO_GCLK state..."
        self.assertEquals(a_pin_group.read(), 3)
        time.sleep(1.0)
        self.assertEquals(a_pin_group.read(0), 0)
 
    def test_04250_blocking_rising_read_word_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rF')
        self.assertIsInstance(a_pin_group,pingroup.PinWordBlockingReader)
        print "\nMake P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(2.5)
        self.assertEquals(a_pin_group.read(), 3)
        print "Toggle P1 pin GPIO_GEN6 state keep   GPIO_GCLK  HIGH..."
        self.assertEquals(a_pin_group.read(), 2)
        print "Keep   P1 pin GPIO_GEN6 HIGH  toggle GPIO_GCLK state..."
        self.assertEquals(a_pin_group.read(), 0)
        time.sleep(1.0)
        self.assertEquals(a_pin_group.read(0), 3)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."

    def test_05100_poll_blocking_read_list_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rBS')
        self.assertIsInstance(a_pin_group,pingroup.PinListBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), [False,False])
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), [True,False])
        print "Make P1 pin GPIO_GEN6  LOW  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), [False,True])
        print "Make P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(0), [True,True])

    def test_05150_blocking_both_read_word_list_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rBS')
        self.assertIsInstance(a_pin_group,pingroup.PinListBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [False,False])
        print "Change P1 pin GPIO_GEN6 to HIGH  keep   GPIO_GCLK at  LOW..."
        self.assertEquals(a_pin_group.read(), [True,False])
        print "Keep   P1 pin GPIO_GEN6 at HIGH  change GPIO_GCLK to HIGH..."
        self.assertEquals(a_pin_group.read(), [True,True])
        print "Change P1 pin GPIO_GEN6 to  LOW  keep   GPIO_GCLK at HIGH..."
        self.assertEquals(a_pin_group.read(), [False,True])

    def test_05200_blocking_rising_read_list_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rRS')
        self.assertIsInstance(a_pin_group,pingroup.PinListBlockingReader)
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."
        time.sleep(1.5)
        self.assertEquals(a_pin_group.read(), [False,False])
        print "Toggle P1 pin GPIO_GEN6 state keep   GPIO_GCLK   LOW..."
        self.assertEquals(a_pin_group.read(), [True,False])
        print "Keep   P1 pin GPIO_GEN6  LOW  toggle GPIO_GCLK state..."
        self.assertEquals(a_pin_group.read(), [True,True])
        time.sleep(1.0)
        self.assertEquals(a_pin_group.read(0), [False,False])

    def test_05250_blocking_rising_read_list_from_gpio_gen6_and_gpio_gclk(self):
        a_pin_group = pingroup.open_pingroup( [ pingroup.PinId.p1_gpio_gen6()\
                                              , pingroup.PinId.p1_gpio_gclk()\
                                              ]\
                                            , 'rFS')
        self.assertIsInstance(a_pin_group,pingroup.PinListBlockingReader)
        print "\nMake P1 pin GPIO_GEN6 HIGH  and GPIO_GCLK HIGH..."
        time.sleep(2.5)
        self.assertEquals(a_pin_group.read(), [True,True])
        print "Toggle P1 pin GPIO_GEN6 state keep   GPIO_GCLK  HIGH..."
        self.assertEquals(a_pin_group.read(), [False,True])
        print "Keep   P1 pin GPIO_GEN6 HIGH  toggle GPIO_GCLK state..."
        self.assertEquals(a_pin_group.read(), [False,False])
        time.sleep(1.0)
        self.assertEquals(a_pin_group.read(0), [True,True])
        print "\nMake P1 pin GPIO_GEN6  LOW  and GPIO_GCLK  LOW..."

if __name__ == '__main__':
    unittest.main()
