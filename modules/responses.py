from modules.base.header import ModbusResponseHeader
from modules.base.inner_fields_response import ModbusResponseFields
from modules.base.crc import ModbusFrameCRC
from modules.defines import ModbusExceptionCodes, ModbusFunctionCode

class BaseModbusResponse:
    
    def __init__(self, buffer : bytes):
        
        self.header : ModbusResponseHeader = None
        self._values : bytes = None
        self.crc : ModbusFrameCRC = None
        
        if len(buffer) >= self.__minimalResponseFrameSize:
            self.header = ModbusResponseHeader(buffer[0], ModbusFunctionCode(buffer[1]), buffer[2])
            self._values = buffer[self.__headerSize : (len(buffer) - self.__crcFieldSize)]
            self.crc = ModbusFrameCRC(self.__parseBuff2Int(buffer[(len(buffer) - self.__crcFieldSize):]))
        
        
    
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
    def values(self) -> bytes:
        return self._values
        
        
    @property
    def payload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.values)
        return buff
    
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.payload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Payload: {}, CRC: {}".format(self.header, self.values.hex(), self.crc)


class ModbusReadCoilsResponse(BaseModbusResponse):

    def __init__(self, buffer):
        super().__init__(buffer)