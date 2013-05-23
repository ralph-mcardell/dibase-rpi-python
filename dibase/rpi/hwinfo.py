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
              a problem initialsing the raw revision value from /proc/cpuinfo.
    '''
    if HwInfo.__raw_revision==None:
      HwInfo.__init_revision_info()
    return HwInfo.__raw_revision

  @classmethod
  def major_revision(cls):
    '''
      Return the major Raspveryy Pi board revision number. This is based on the
      raw revision number. To date (Mat 2013) there are two major revisions of 
      Raspberry Pi boards:
        1 : raw revisions 1..3 inclusive
        2 : raw revisions greater than 3
     returns 1 or 2 or None if the raw revision value is None, indicating it
            could not be determined.
    '''
    raw_rev = HwInfo.raw_revision()
    if raw_rev==None:
      return None
    elif raw_rev<=3:
      return 1
    else:
      return 2

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
