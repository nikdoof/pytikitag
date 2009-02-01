import mifareul
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUltralight):

    def get_uid(self):
            d = self.read_block(0)
            d = d+ self.read_block(1)        

            return toHexString(d).replace(" ", "")[:16]
