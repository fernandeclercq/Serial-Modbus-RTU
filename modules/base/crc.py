
from ctypes import *
from crc import Calculator, Crc16
mb_crc_calculator = Calculator(Crc16.MODBUS)

class BaseModbusFrameCRCFields(BigEndianStructure):
    _fields_ = [
        ('_u16_crc', c_uint16)
    ]
    
    @property
    def _crc(self) -> int:
        return self._u16_crc
    
    @_crc.setter
    def _crc(self, new_val : int):
        self._u16_crc = new_val

    def __str__(self):
        return "CRC: {}".format(hex(self._crc))
    
    
    
class BaseModbusFrameCRCUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusFrameCRCFields),
        ('_data', c_uint8 * sizeof(BaseModbusFrameCRCFields))
    ]
    
    @property
    def fields(self) -> BaseModbusFrameCRCFields:
        return self._fields
    
    @property
    def crc(self):
        return self.fields._crc
    
    @property
    def data(self) -> bytes:
        return bytes(self._data)
    
    @property
    def dataSwapped(self) -> bytes:
        temp : bytearray = bytearray(self.data)
        temp.reverse()
        return bytes(temp)
    
    @property
    def crcSwapped(self) -> int:
        return int( (self.dataSwapped[0] << 8) | (self.dataSwapped[1]) )
        
    @classmethod
    def fieldSize(cls) -> int:
        """Returns the size of the CRC Fields as an integer

        Returns:
            int: An integer value
        """
        return sizeof(cls)
    
    def generateCrc(self, payload : bytes):
        """Generates CRC for a Modbus Frame based on the payload and saves it to the CRC Field

        Args:
            payload (bytes): A readable bytes buffer
        """
        raw_result : int = 0
        raw_result = mb_crc_calculator.checksum(payload)
        self.fields._crc = int( ((raw_result >> 8) & 0xFF) | ((raw_result << 8) & 0xFF00) )
        
        
    def verifyCrc(self, payload : bytes) -> bool:
        """Verifies the CRC against a calculated CRC from the given payload

        Args:
            payload (bytes): A readable buffer of bytes

        Returns:
            bool: Returns True if the CRC Matches the calculated CRC. Otherwise False is returned
        """
        verify_result : bool = False
        calculated_crc : int = mb_crc_calculator.checksum(payload)
        
        if calculated_crc == self.crcSwapped:
            verify_result = True
        
        return verify_result
    
    def __str__(self):
        return "{}".format(self.fields)
    
    
class ModbusFrameCRC(BaseModbusFrameCRCUnion):
    def __init__(self, crc_u16 : int = 0):
        self.fields._crc = crc_u16
        
    def __str__(self):
        return super().__str__()