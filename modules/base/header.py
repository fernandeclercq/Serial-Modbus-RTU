from ctypes import *

from modules.defines import ModbusFunctionCode, ModbusExceptionCodes
from modules.generic import BaseLabelEnum

class BaseModbusFrameHeaderFields(BigEndianStructure):
    _fields_ = [
        ('_slave_address', c_uint8),
        ('_function_code', c_uint8),
    ]
    
    @property
    def _slaveAddress(self) -> int:
        return self._slave_address
    
    @property
    def _functionCode(self) -> int:
        return self._function_code
    
    def __str__(self):
        return "Slave Address: {}, Function Code: {}".format(self._slaveAddress, self._functionCode)
    

class BaseModbusFrameHeaderUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusFrameHeaderFields),
        ('_data', c_uint8 * sizeof(BaseModbusFrameHeaderFields))
    ]
    
    @property
    def fields(self) -> BaseModbusFrameHeaderFields:
        return self._fields
    
    @property
    def slaveAddress(self) -> int:
        return self.fields._slaveAddress
    
    @property
    def functionCode(self) -> int:
        return self.fields._functionCode
    
    
    @classmethod
    def fieldsSize(cls) -> int:
        """Returns the size of the header fields

        Returns:
            int: An integer value
        """
        return sizeof(cls)
    
    @property
    def hasErrors(self) -> bool:
        if self.functionCode & 0x80:
            return True
        return False
    
    @property
    def isBroadcast(self) -> bool:
        if self.slaveAddress == 0x00:
            return True
        return False


    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    
    def __str__(self):
        return "{}".format(self.fields)
    
    
    
class ModbusFrameHeader(BaseModbusFrameHeaderUnion):
    def __init__(self, slave_id : int, function_code : BaseLabelEnum):
        self.fields._slave_address = slave_id
        self.fields._function_code = function_code.value
        
    def __str__(self):
        return super().__str__()
    
    
########################################################################################

class BaseModbusResponseHeaderFields(BaseModbusFrameHeaderFields):
    _fields_ = [
        ('_byte_count__exception_code_', c_uint8)
    ]
    
    @property
    def _byteCount(self) -> int:
        return self._byte_count__exception_code_
    
    @_byteCount.setter
    def _byteCount(self, new_val : int):
        self._byte_count__exception_code_ = new_val
    
    @property
    def _exceptionCode(self) -> int:
        return self._byteCount
    
    @_exceptionCode.setter
    def _exceptionCode(self, new_val : int):
        self._byte_count__exception_code_ = new_val
        
    
class BaseModbusResponseHeaderUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusResponseHeaderFields),
        ('_data', c_uint8 * sizeof(BaseModbusResponseHeaderFields))
    ]
    
    @property
    def fields(self) -> BaseModbusResponseHeaderFields:
        return self._fields
    
    @property
    def slaveAddress(self) -> int:
        return self.fields._slaveAddress
    
    @property
    def functionCode(self) -> int:
        return self.fields._functionCode
    
    @property
    def byteCount(self) -> int:
        return self.fields._byteCount
    
    @property
    def exceptionCode(self) -> int:
        return self.fields._exceptionCode
    
    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    @classmethod
    def fieldsSize(cls):
        return sizeof(cls)
    
    @property
    def hasErrors(self) -> bool:
        if self.functionCode & 0x80:
            return True
        return False
    
    @property
    def isBroadcast(self) -> bool:
        if self.slaveAddress == 0x00:
            return True
        return False
    
    
    
    
    def __str__(self):
        if self.hasErrors:
            return "Slave Id: {}, Function Code: {}, Exception Code: {}".format(
                self.slaveAddress, self.functionCode, self.exceptionCode
            )
        else:
            return "Slave Id: {}, Function Code: {}, Byte count: {}".format(
                self.slaveAddress, self.functionCode, self.byteCount
            )
        
    
class ModbusResponseHeader(BaseModbusResponseHeaderUnion):
    def __init__(self, slave_id : int, function_code : BaseLabelEnum, byte_count__exception_code : int):
        self.fields._slave_address = slave_id
        self.fields._function_code = function_code.value
        self.fields._byteCount = byte_count__exception_code
        
    def getExceptionCode(self) -> ModbusExceptionCodes:
        return ModbusExceptionCodes(self.fields._exceptionCode)
        
    def __str__(self):
        return super().__str__()