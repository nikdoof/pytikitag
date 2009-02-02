import ndef

class NFCType2():

    tags = []
    ndefs = []   

    def __init__(self, data):
               
        if not data:
            raise ValueError
        
        # Minimum requirement is 6 x 4 byte pages to meet Type2 style tags    
        if len(data) > 6 * 4:
        
            # Set inital start point for a Type2, based on 3 pages of reserved
            # data
            i = 13
        
            while i <= len(data)-1:
                if data[i] == 0x00:
                    # Null, skip
                    i = i + 1
    
                elif data[i] == 0x03:
                    # NDEF start tag
                    if data[i+1] == 0xFF:
                        # Multibyte length
                        tlv_len = data[i+2:i+3]
                        i = i + 4
                    else:
                        tlv_len = data[i+1]
                        i = i + 2

                    tlv_data = data[i:i+tlv_len]
                    
                    i = i + tlv_len
                    
                    self.tags.append([0x03, tlv_data])
                    
                elif data[i] == 0xFE:
                    break
                
                else:
                    i = i + 1
                    
        for tag in self.tags:
            if tag[0] == 0x03:
                self.ndefs.append(ndef.NDEFReader(tag[1]))
