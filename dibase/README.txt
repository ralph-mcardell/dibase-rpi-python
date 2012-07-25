===================================
Dibase Raspberry Pi Python Services
===================================

The Dibase Raspberry Pi Python services are intended as
a collection of various services for the Raspberry Pi in
the containing nested packages dibase.rpi - in order to
note them as Raspberry Pi specific and differentiate them
from Raspberry Pi packages from other parties.

The initial version includes one package within the
dibase.rpi containing package: gpio.

GPIO services: dibase.rpi.gpio
==============================

The *dibase.rpi.gpio* package provides facilities for accessing
the general purpose IO lines available on the Raspberry Pi
using the Linux user space support provided in the sys file
system in the form of IO classes similar in style to the Python
file type (or various file IO types in Python 3).

Pin ids : modeule pinid
------------------------

GPIO lines are identified by integer pin id values rather than
path name strings. The *PinId* class in the *pinid* module
provides support for such values ensuring they are valid and
providing class methods to create pin id values representing
the pins on the Raspberry Pi's P1 26 pin header connector.

Single GPIO pin IO : module pin
-------------------------------

The main GPIO types and functions are defined in the *pin*
module.

The *open_pin* function is similar in style to the Python
built in open function for files et al. It takes a pin id value
- either an integer or a *pinid.PinId* instance, and a mode
string which can be 0, 1 or 2 characters long. The first
mode string character indicates the data direction:

* 'w' indicates we want to write (or output) to the pin

* 'r' indicates we wish to read (or input) from the pin (default)

Note that a pin is open either for writing OR reading but not
both. Each pin represents one binary bit so is read or written
as a boolean: True, False. When writing any value that can be
converted to a boolean can be used: 0, 1 or any other non zero
value or '0', '1'. Note that '0' is a special case as usually
it would be interpreted as True but will be written as a False
value.

Writing to a pin changes the pin value immediately (as
immediately as writing to a sys filesystem file causing a
change to the associated memory mapped register bit).

Reading is as fast as reading from a sys file system file and
will **not** wait for a change to the pin state before
returning.

However, GPIO pins can be setup to notify on changes to pin
state and this is supported in the sys filesystem. It is only
relevant to input values - as changes to written values to
output pins could have notification handled elsewhere by
software. To take advantage of pin state change notifications
we can request a pin be opened with a wait mode value by
providing a second character in the open mode string:

* 'N' indicates no wait mode. Only mode supported for writable
  pins (default)

* 'R' wait for rising edge state transitions - i.e. when the
  input value changes from 0 to 1

* 'F' wait for falling edge state transitions - i.e. when the
  input value changes from 1 to 0

* 'B' wait for both (or either) edge state transitions

Note that if no mode string value is passed or an empty mode
string passed then the default direction and wait modes are
used: 'rN' : open for reading (input), not waitable.

The object returned from open_pin will have operations
pertinent to the requested open mode, so a pin opened for
writing will have a write operation but no read or wait
operations.

A read pin opened that is not waitable will have a read
operation but no write or wait operations.

A read pin opened that is waitable will have read and wait
operations but no write operation.

All such objects can be queried to determine if they are
readable, writeable, waitable or closed and for the underlying
OS file descriptor number representing the file descriptor used
to access the GPIO pin's sys file system *value* file. Unlike
some other Raspberry Pi Python GPIO packages pin IO objects
returned from open_pin should be closed when no longer
required. They will be closed when (if!!) the object is
destroyed and all such types support automatic cleanup via the
Python *with* feature.

Note that failure to close a pin can prevent it being opened
again by another process - which might happen on a bad exit
from an application. In order to cleanup such bad in-use pins
the function force_free_pin can be used.
