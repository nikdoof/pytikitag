import sys
import logging
from smartcard.System import readers
from smartcard.util import toHexString, toASCIIString

class TikiReader():
    
    _logger = logging.getLogger('pytikitag.reader')
    _readers = None
    _tiki_rfid_apdu_cmd = [0xFF, 0x00, 0x00, 0x00]
    _tiki_rfid_apdu_resp = [0xFF, 0xC0, 0x00, 0x00]
    
    def __init__(self, readerid = 0):
        
        self._readers = readers()
        self._connection = self._readers[readerid].createConnection()
        
        self._connection.connect()
        
    def trans_raw(self, cmd):
        """Transmit a raw APDU command via the RFID interface of the device"""
    
        return self._connection.transmit(cmd)
        
    def trans_rfid(self, cmd):
        """Transmit command via RFID and return the data"""       
               
        if self._connection:
            fcmd = self._build_cmd(1, cmd)
            self._logger.debug("Sending command: %s" % toHexString(fcmd))
            resp, s1, s2 = self.trans_raw(fcmd)

        self._logger.debug("Response: %x %x" % (s1, s2))
        if s1 == 0x61:
            self._logger.debug("Sending command: %s" % toHexString(self._build_cmd(2, [s2])))
            data, s1, s2 = self.trans_raw(self._build_cmd(2, [s2]))
            return data
        elif s1 == 0x63:
            if s2 == 0x00:
                return -1
            elif s2 == 0x01:
                return -2
        else:
            return -3                     
            
    def firmware_version(self):
        """Retreives the firmware version of the ACR122/Tikitag Reader"""
        resp, s1, s2 = self._connection.transmit([0xFF, 0x00, 0x00, 0x48, 0x00, 0x00])

        if not s1 == 99:
            return resp
        else:   
            return None
            
    def _build_cmd(self, type, cmd):

        if type == 1:
            prefix = self._tiki_rfid_apdu_cmd 
            fcmd = prefix + [len(cmd)] + cmd
        elif type == 2:
            prefix = self._tiki_rfid_apdu_resp 
            fcmd = prefix + cmd
        
        return fcmd
    

