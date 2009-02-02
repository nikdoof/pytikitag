from smartcard.util import toASCIIString

class NDEFReader():

    _records = []
    items = []

    _uri_lookup = { 0x00: "", 0x01: "http://www.", 0x02: "https://www.",
                    0x03: "http://", 0x04: "https://", 0x05: "tel:",
                    0x06: "mailto:", 0x07: "ftp://anonymous:anonymous@",
                    0x08: "ftp://ftp.", 0x09: "ftps://", 0x0A: "sftp://",
                    0x0B: "smb://", 0x0C: "nfs://", 0x0D: "ftp://",
                    0x0E: "dav://", 0x0F: "news:", 0x10: "telent://",
                    0x11: "imap:", 0x12: "rtsp://", 0x13: "urn:",
                    0x14: "pop:", 0x15: "sip:", 0x16: "sips:",
                    0x17: "tftp:", 0x18: "btspp://", 0x19: "btl2cap://",
                    0x1A: "btgoep://", 0x1B: "tcpobex://", 0x1C: "irdaobex://",
                    0x1D: "file://", 0x1E: "urn:epc:id:", 0x1F: "urn:epc:tag:",
                    0x20: "urn:epc:pat:", 0x21: "urn:epc:raw:", 0x22: "urn:epc:",
                    0x23: "urn:nfc:" }

    def _parse_item(self, item):
        
        item_type = item[1]
        item_value = item[2]
        
        if item_type == 0x55:
            # URL Type
            if not item_value[0] > 0x23:
                url = self._uri_lookup[item_value[0]] + toASCIIString(item_value[1:])
            else:
                url = toASCIIString(item_value)
            
            self.items.append(["url", url])
    
                
    def __init__(self, ndef):

        if not ndef:
            raise ValueError
    
        i = 0
            
        while i <= len(ndef)-1:
        
            if ndef[i] == 0xD1:
                ndef_mb = ndef[i+1]
                ndef_len = ndef[i+2]
                ndef_type = ndef[i+3]
                ndef_value = ndef[i+4:i+4+ndef_len]
                
                self._records.append([ndef_mb, ndef_type, ndef_value])
                
                i = i + 4 + ndef_len
            else:
                i = i + 1
                
        for item in self._records:
            self._parse_item(item)
            
            
