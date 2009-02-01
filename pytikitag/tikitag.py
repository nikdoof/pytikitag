import mifareul
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUL):

    def tag_id(self):
            d = self.read_block(0)        

            return toHexString(d).replace(" ", "")[:16]
