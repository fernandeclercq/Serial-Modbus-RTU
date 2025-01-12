from modules.base.header import ModbusResponseHeader
from modules.base.inner_fields_response import ModbusResponseFields
from modules.base.crc import ModbusFrameCRC
from modules.defines import ModbusExceptionCodes, ModbusFunctionCode

import math

class BaseModbusResponse:
    
    def __init__(self, buffer : bytes):
        
        self.header : ModbusResponseHeader = None
        self._values : bytes = None
        self.crc : ModbusFrameCRC = None
        
        if len(buffer) >= self.__minimalResponseFrameSize:
            self.header = ModbusResponseHeader(buffer[0], ModbusFunctionCode(buffer[1]), buffer[2])
            self._values = buffer[self.__headerSize : (len(buffer) - self.__crcFieldSize)]
            self.crc = ModbusFrameCRC(self.__parseBuff2Int(buffer[(len(buffer) - self.__crcFieldSize):]))
            
        else:
            self.header = ModbusResponseHeader(0x00, ModbusFunctionCode.ERROR_NO_FC, 0x00)
            self._values = bytes([0x00])
            self.crc = ModbusFrameCRC(0x00)
        
        
    
    def __parseBuff2Int(self, buff : bytes, swapped : bool = False) -> int:
        result : int = 0
        
        if swapped:
            result = ((buff[1] << 8 & 0xFF00) | (buff[0] & 0xFF))
            
        else:
            result = ((buff[0] << 8 & 0xFF00) | (buff[1] & 0xFF))
        
        return result
    
    @property
    def __headerSize(self) -> int:
        return ModbusResponseHeader.fieldsSize()
    
    
    @property
    def __crcFieldSize(self) -> int:
        return ModbusFrameCRC.fieldSize()
    
    
    @property
    def __minimalResponseFrameSize(self) -> int:
        return (self.__headerSize + self.__crcFieldSize)


    @property
    def payload(self) -> bytes:
        return self._values
        
        
    @property
    def dataHeaderPayload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.payload)
        return buff
    
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.dataHeaderPayload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Payload: {}, CRC: {}".format(self.header, self.payload.hex(), self.crc)





class BaseModbusReadBitsResponse:

    def __init__(self, buffer : bytes):
        self._baseResponse : BaseModbusResponse = BaseModbusResponse(buffer)
        
        
    def _getBit(self, coil_position : int = 0):
        
        byte_pos_idx : int = (math.floor(coil_position / 8))
        shift_right_amount = (coil_position % 8)
    
        if len(self.payload) > byte_pos_idx:
            return ( self.payload[byte_pos_idx] >> shift_right_amount ) & 0x01
        
        else:
            return None
        
    @property
    def payload(self) -> bytes:
        return self._baseResponse.payload
        
    @property
    def rawData(self) -> bytes:
        return self._baseResponse.data
    
    @property
    def hasErrors(self) -> bool:
        return self._baseResponse.header.hasErrors
    
    def __str__(self):
        return self._baseResponse.__str__()    
    
    
class BaseModbusReadRegistersResponse:
    def __init__(self, buffer : bytes):
        self._baseResponse : BaseModbusResponse = BaseModbusResponse(buffer)
        
    def _getRegister(self, register : int = 0) -> int | None:
        result : int = None
        LSB_idx = (2 * register)
        MBS_idx = (2 * register) + 1
        
        if MBS_idx <= len(self.payload):
            lsb_byte : bytes = self.payload[MBS_idx]
            msb_byte : bytes = self.payload[LSB_idx]
            result = int( (msb_byte << 8) | (lsb_byte) )
        
        return result
        

    @property
    def payload(self) -> bytes:
        return self._baseResponse.payload
        
    @property
    def rawData(self) -> bytes:
        return self._baseResponse.data
    
    @property
    def hasErrors(self) -> bool:
        return self._baseResponse.header.hasErrors
    
    def __str__(self):
        return self._baseResponse.__str__()
    
    
    
    
    
    
    

    
class ModbusReadCoilsResponse(BaseModbusReadBitsResponse):
    def __init__(self, buffer : bytes):
        super().__init__(buffer)
        
        
    def getCoil(self, coil_pos : int = 0):
        return self._getBit(coil_pos)
    
    
    
class ModbusReadInputRegistersResponse(BaseModbusReadRegistersResponse):
    def __init__(self, buffer : bytes):
        super().__init__(buffer)
        
    def getRegister(self, register : int = 0) -> int | None:
        return self._getRegister(register)
    
    
class ModbusReadHoldingRegistersResponse(BaseModbusReadRegistersResponse):
    def __init__(self, buffer : bytes):
        super().__init__(buffer)
        
    def getRegister(self, register : int = 0) -> int | None:
        return self._getRegister(register)
    