#!/usr/bin/python
import logging, sys
from pytikitag import reader, tikitag
from pytikitag.nfc import type2
from smartcard.util import toHexString, toASCIIString

log = logging.getLogger('pytikitag.mifareul')
h = logging.StreamHandler(sys.stdout)
log.addHandler(h)

r = reader.TikiReader()
m = tikitag.TikiTag(r)

print "Tikitag ID: " + m.get_uid()
print "Manf: " + m.get_manf_ascii() + ", Serial: " + m.get_serial()
print ""
print "Reading Tikitag Data..."
print m.get_tag_url()

#tag = type2.NFCType2(d)
#print tag.ndefs[0].items
#print toHexString(value)
#print toASCIIString(value)
