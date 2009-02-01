#!/usr/bin/python

from pytikitag import reader, tikitag
from smartcard.util import toHexString, toASCIIString

m = tikitag.TikiTag()

print m.get_uid()

d = m.read_tag()
print "%s bytes" % len(d)
print toHexString(d)

