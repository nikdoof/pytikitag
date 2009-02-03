import mifareul
from nfc import type2, ndef
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUltralight):

    _tag = None
    _uid = ""

    def get_uid(self):
    
            d = self.read_block(0)
            d = d+ self.read_block(1)        
            
            uid = toHexString(d).replace(" ", "")[:16]

            return uid
                        
    def get_tag_url(self):
        """ Retreives the tag's URL stored in NDEF format """
        
        # The tikitag usually has a single NDEF with a single URI record type
        # so assumptions can be made here.
      
        d = self.read_tag()
        self._tag = type2.NFCType2(d)
    
        return self._tag.ndefs[0].items[0][1]
        
        
    
