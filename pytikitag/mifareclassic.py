import logging
import reader
import time
from smartcard.util import toHexString

class MiFareClassic():
    """"""
       
    _logger = logging.getLogger('pytikitag.mifareclassic')
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
          

    def read_id(self):
        
        d = self._reader.trans_rfid([0xD4, 0x4A, 0x01, 0x00])
        
        if d:
            return toHexString(d)
            
            


