import logging
import reader
import time
from smartcard.util import toHexString

class MiFareUltralight():
    """Class to control MiFare Ultralight RFID Tags
       
       The Ultralights have 64 bytes storage with 10 bytes being unwritable
       (page 0x0-0x1 and first two bytes of 0x2) and 4 bytes allocated to OTP 
       (page 0x3)
       
       Specifications: http://www.nxp.com/products/identification/mifare/ultralight/"""
       

    _logger = logging.getLogger('pytikitag.mifareul')
    _reader = None
    
    _manf_ids = {0x04: "NXP / Phillips"}

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
          

    def get_manf(self):
        """Get the IC manufacturer"""
        return self.read_block(0x0)[0]
    
    def get_manf_ascii(self):
        mid = self.get_manf()
        if mid:
            return self._manf_ids[mid]
        else:
            return None
        
    def get_serial(self):
        """Get the serial number of the IC"""
        # MiFare Serials are stored in page 0x0 and 0x1, the format is as follows
        # MF,S1, S2, C1   S4, S5, S6
        #
        # Where MF is the manufacturer ID, S is a serial value and C is a check byte
        
        d1 = self.read_block(0x0)
        d2 = self.read_block(0x1)
        
        sn = toHexString(d1[1:3] + d2)
        return sn.replace(" ", "")        
            
    def read_block(self, block, timeout = 100):
        """Reads a full 4 byte page from the RFID tag"""
        
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
                    
    def write_block(self, block, data, confirm=True):
        """Write a full 4 byte page to the writable area of the tag"""
        if block < 0x4 or block > 0xf:
            raise ValueError("Invalid block")   
      
        if len(data) > 4:
            raise ValueError("Data is larger than 4 bytes")
        
        i = 1  
            
        while i <= 16-len(data):
            data = data + [0x00]
      
        self._logger.debug("Writing data: %s" % data)
        d = self._reader.trans_rfid([0xD4, 0x40, 0x01, 0xA0] + [block] + data)
        
        if confirm:        
            if data[:4] == self.read_block(block):
                return True
            else:
                return False
        else:
            return True

    def read_tag(self):
            
            i = 0
            d = []
            
            while i <= 16:
                d = d + self.read_block(i)
                i = i + 1
                
            return d
                

