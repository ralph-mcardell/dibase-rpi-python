'''
    Part of the dibase.rpi package.

    Raspberry Pi hardware information
    Provides functions to return various Raspberry Pi specific hardware
    values such as board revision values.

    Developed by R.E. McArdell / Dibase Limited.
    Copyright (c) 2012 Dibase Limited
    License: dual: GPL or BSD.
'''

class HwInfo(object):
  '''
    Class encapsulating various Raspberry Pi hardware specific properties
  '''
  @classmethod
  def raw_revision(cls):
    '''
      Return the raw revision value as a positive integer as indicated by the
      /proc/cpuinfo pseudo file Revision field line.
      returns a positive integer greater or equal to 1, or None if there was
              a problem initialising the raw revision value from /proc/cpuinfo.
    '''
    if HwInfo.__raw_revision==None:
      HwInfo.__init_revision_info()
    return HwInfo.__raw_revision

  @classmethod
  def major_revision(cls):
    '''
      Return the major Raspberry Pi board revision number. This is based on the
      raw revision number. To date there are five major revisions of 
      Raspberry Pi boards:
        1 : raw revisions 1..3 inclusive (Original model B & A)
        2 : raw revisions greater than 3 up to and including 15 (B, A rev 2)
        3 : raw revisions 16, 18, and greater: B+, A+ and R'Pi 2.0 B
            (raw revision range unknown at time of writing but presumed to be
             greater than 0x12 and presumed compatible with B+ GPIO)
        4: raw revision 17 (0x11) : Raspberry Pi compute module - intended to
           be part of other designs.
        5 : raw revisions greater than 18 (0x12): R'Pi 2.0 B and beyond
            (raw revision range unknown at time of writing but presumed to be
             greater than 0x12 and presumed compatible with B+ GPIO)
     returns value in range [1,5] or None if the raw revision value is None,
             indicating it could not be determined.
    '''
    raw_rev = HwInfo.raw_revision()
    if raw_rev==None:
      return None
    elif raw_rev<=3:
      return 1
    elif version>3 and version<=0xf:
      return 2
    elif version==0x10 or version==0x12: # B+, A+
      return 3
    elif version==0x11: # compute module
      return 4
    else: # Raspberry Pi 2.0 B etc. ?
      return 5

  @classmethod
  def gpio_revision(cls):
    '''
      Maps Raspberry Pi major board revision values to major GPIO connector
      changed. To date there are 4 GPIO scenarios:
        1 : Major revision 1 (Original model B & A) : 26 pin P1
        2 : Major revision 2 (B, A) Tweaks P1 pin GPIO assignments, adds P5
        3 : Major revision 3 (B+< A+) + Raspberry Pi 2.0 B : 40 pin J8,
            First 26 pins compatible with Rev. 2 P1. Looses P5.
        4: Compute module: Has no GPIO connector of its own other than all GPIO
           pins brought out to 200 pin edge connector for use as required in 
           3rd party hardware.
      returns value in range [1,4] or None if the raw revision value is None,
             indicating it could not be determined. Value is same as
             major_revision, unless major_revision returns 5 in which case 3 
             is returned.
    '''
    gpio_version = HwInfo.major_revision()
    if gpio_version == 5:
      gpio_version = 3
    return gpio_version

  @classmethod
  def __init_revision_info(cls):
    '''
      Internal private method to open /proc/cpu info and extract the Revision
      hexadecimal integer string value and cache it as an int.
    '''
    with open('/proc/cpuinfo','r') as cpuinfo:
      line = line=cpuinfo.readline()
      while line!='':
        field = line.split()
        if len(field)>=3 and field[0]=='Revision':
          HwInfo.__raw_revision = int(''.join(['0x',field[2]]),0)
          break
        line = line=cpuinfo.readline()

  __raw_revision = None
