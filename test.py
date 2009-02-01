#!/usr/bin/python
import logging, sys
from pytikitag import reader, tikitag
from smartcard.util import toHexString, toASCIIString

log = logging.getLogger('pytikitag.mifareul')
h = logging.StreamHandler(sys.stdout)
log.addHandler(h)

r = reader.TikiReader()

print r.firmware_version()

m = tikitag.TikiTag(r)

print m.get_uid()

#d = m.read_tag()
#print "%s bytes" % len(d)
#print toHexString(d)

print m.write_block(0xf, [0xde, 0xad, 0xbe, 0xee])

print toHexString(m.read_block(0xf))
