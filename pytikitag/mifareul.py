import logging
import reader
import time
from smartcard.util import toHexString, toASCIIString

class MiFareUL():

    _logger = logging.getLogger('pytikitag.mifareul')
    _reader = None

    def __init__(self, pcscreader=None):
        

        if not pcscreader:
            self._reader = reader.TikiReader()
        else:
            self._reader = pcscreader  
        
    def _tag_available(self):
        
        if self._reader.trans_rfid([0xD4, 0x4A, 0x01, 0x00])[2] > 0x00:
            return True
        else:
            return False
            
    def read_block(self, block, timeout = 100):
        """Reads a full 8 byte page from the RFID tag"""
        
        d = None
        t = 0
    
        while not self._tag_available():
            pass
    
        while not d:
            d = self._reader.trans_rfid([0xD4, 0x40, 0x01, 0x30] + [block])

        if d:
            return d[3:7]
        else:
            return None
                    
    def write_block(self, block, data):
        """Write a full 4 byte page to the writable area of the tag"""
        if block < 0x04:
            raise ValueError("Invalid block")
      
        pass
        d = self._reader.trans_rfid([0xD4, 0x40, 0x01, 0xA0] + [block] + data)
        
    def read_tag(self):
            
            i = 0
            d = []
            
            while i <= 16:
                d = d + self.read_block(i)
                i = i + 1
                
            return d
                

