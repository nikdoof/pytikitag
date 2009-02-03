import mifareul
from nfc import type2, ndef
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUltralight):

    _tag = None
    _uid = None

    def get_uid(self):
    
            d = self.read_block(0)
            d = d+ self.read_block(1)        
            
            uid = toHexString(d).replace(" ", "")[:16]

            return uid
    
    def _check_uid(self):
        uid = self.get_uid()
        if (not self._uid == uid):
            self._tag = None
            self._uid = uid  
            return False
        else:
            return True  
            
    def get_tag_url(self):
        """ Retreives the tag's URL stored in NDEF format """
        
        # The tikitag usually has a single NDEF with a single URI record type
        # so assumptions can be made here.
        
        self._check_uid()
               
        if not self._tag:
            d = self.read_tag()
            self._tag = type2.NFCType2(d)
    
        return self._tag.ndefs[0].items[0][1]
        
        
    
