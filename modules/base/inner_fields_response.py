from ctypes import *

from modules.defines import ModbusExceptionCodes

class BaseModbusResponseFields(BigEndianStructure):
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
        
    
    def __str__(self):
        return "{}".format(self._byteCount)
    

class BaseModbusResponseUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusResponseFields),
        ('_data', c_uint8 * sizeof(BaseModbusResponseFields))
    ]
    
    @property
    def fields(self) -> BaseModbusResponseFields:
        return self._fields
    
    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    @classmethod
    def fieldsSize(cls):
        return sizeof(cls)
    
    def __str__(self):
        return "{}".format(self.fields, self.rawData)
    

class ModbusResponseFields(BaseModbusResponseUnion):
    def __init__(self, byte_count__exception_code : int):
        self.fields._byteCount = byte_count__exception_code
        
    def getExceptionCode(self) -> ModbusExceptionCodes:
        return ModbusExceptionCodes(self.fields._exceptionCode)
    
    def __str__(self):
        return super().__str__()