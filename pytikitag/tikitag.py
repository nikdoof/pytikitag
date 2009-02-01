import mifareul
from smartcard.util import toHexString, toASCIIString 

class TikiTag(mifareul.MiFareUltralight):

    def get_uid(self):
            d = self.read_block(0)
            d = d+ self.read_block(1)        

            return toHexString(d).replace(" ", "")[:16]
            
    def get_tag_url(self):
            if toASCIIString(self.read_block(0x6)) == "tag.":
                return "http://ttag.be/m/%s" % self.get_uid()
