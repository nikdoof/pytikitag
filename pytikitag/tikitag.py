import mifareul
from nfc import type2, ndef
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUltralight):

    def get_uid(self):
            d = self.read_block(0)
            d = d+ self.read_block(1)        

            return toHexString(d).replace(" ", "")[:16]
            
    def get_tag_url(self):
        
        self._tag = type2.NFCType2(self.read_tag())
        return self._tag.ndefs[0].items[0][1]
        
        
    
