===================================
Dibase Raspberry Pi Python Services
===================================

The Dibase Raspberry Pi Python services are intended as
a collection of various services for the Raspberry Pi in
the containing nested packages dibase.rpi - in order to
note them as Raspberry Pi specific and differentiate them
from Raspberry Pi packages from other parties.

The initial versions include one package within the
dibase.rpi containing package: gpio.

2012-08-15: Added pingroup module to handle multiple GPIO pins
2012-07-25: Initial version handling only single GPIO pins

GPIO services: dibase.rpi.gpio
==============================

The *dibase.rpi.gpio* package provides facilities for accessing
the general purpose IO lines available on the Raspberry Pi
using the Linux user space support provided in the sys file
system in the form of IO classes similar in style to the Python
file type (or various file IO types in Python 3).

Pin ids : module pinid
-----------------------

GPIO lines are identified by integer pin id values rather than
path name strings. The *PinId* class in the *pinid* module
provides support for such values ensuring they are valid and
providing class methods to create pin id values representing
the pins on the Raspberry Pi's P1 26 pin header connector.

Single GPIO pin IO : module pin
-------------------------------

The main GPIO types and functions dealing with IO for single
GPIO pins are defined in the *pin* module.

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
we can request a pin be opened with a blocking mode value by
providing a second character in the open mode string:

* 'N' indicates no edge state transition events are raised and
  so reads will be non-blocking polling mode. Only mode
  supported for writable pins. (default)

* 'R' Raise rising edge state transitions events - i.e. when
   the input value changes from 0 to 1

* 'F' Raise falling edge state transitions events - i.e. when
  the input value changes from 1 to 0

* 'B' Raise events for both edge state transitions

Note that if no mode string value is passed or an empty mode
string passed then the default direction and wait modes are
used: 'rN' : open for reading (input), non-blocking.

The object returned from open_pin will have operations
pertinent to the requested open mode, so a pin opened for
writing will have a write operation but no read
operations.

A read pin opened for reading with no edge state transition
events will have a non-blocking read operation but no write
operation.

A read pin opened for reading with edge state transition
events will have a blocking read operation but no write
operation.

All such objects can be queried to determine if they are
readable, writable, blocking or closed and for the underlying
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

IO for groups of GPIO pins : module pingroup
--------------------------------------------

The main GPIO types and functions dealing with IO for groups
of GPIO pins are defined in the *pingroup* module. Pin groups
make writing to or reading from multiple pins convenient.

The *open_pingroup* function is similar to the *open_pin*
function of the *pin* module. It takes an iterable sequence of
pin id values - either integers or a *pinid.PinId* instances, and
a mode string which can be 0..3 characters long. The mode value
applies to all pins in a pin group. The modes allowed are an
extension of those defined for the *pin* module *open_pin*
function's *mode* parameter. In addition to 'r' and 'w' direction
and 'N', 'R', 'F', 'B' blocking modes, the *open_pingroup* *mode*
parameter also defines a data format mode, which for a fully
specified mode string is given by the 3rd character:

* 'I' indicates a data format of integer words

* 'S' indicates a data format of sequences of Boolean values

The default is a data format of 'I' - integer words.

If the blocking mode is defaulted then the data format mode
character may appear as the 2nd mode string character.

If using an integer word data format then the values of the
individual GPIO pins passed to write or returned from read are
multiplexed into a single integer value where bit 0 (the least
significant bit) of the word contains the value for the GPIO pin
specified by the first (0th) item in the *open_pingroup* pin id
sequence parameter, bit 1 the value for the pin with the id at
element with index 1 in the pin id sequence and so on.

If using an iterable sequence of Boolean values to represent the
values of the individual GPIO pins passed to write or returned
from read then the items in such sequences are taken to be
in the same order in relation to GPIO pins as the pin ids sequence
passed to *open_pingroup*.

The object returned from *open_pingroup* will have operations
pertinent to the requested open mode, so a pin opened for
writing will have a write operation but no read
operations. 

A read pin opened for reading with no edge state transition
events will have a non-blocking read operation but no write
operation. 

A read pin opened for reading with edge state transition
events will have a blocking read operation but no write
operation.

Write will accept an integer if opened specifying an integer word
data format or an iterable sequence if opened specifying a
sequence data format.

Read will return an integer if opened specifying an integer word
data format or an iterable sequence (currently a list) if opened
specifying a sequence data format.

When reading in blocking mode read blocks until either a time out
or *any* pin in the group generates an event. The returned value
tracks changes due to notified events unless a polling read is
performed (by specifying a 0 time out value), when all pins in
the group are polled for their current value. An effect of this
behaviour is that when only waiting for rising edge events or
falling edge events the returned value does *not* directly
reflect the current state of all pins in the group.

Like single pin IO objects returned from *pin.open_pin* objects
returned from *open_pingroup* can be queried to determine if they
are readable, writable, blocking or closed and for the
descriptors used to access GPIO pins' sys file system *value*
file. Objects returned from *open_pingroup* have similar close
requirements and behaviour to objects returned from
*pin.open_pin*.



