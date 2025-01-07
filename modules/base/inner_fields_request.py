from ctypes import *


class BaseModbusReadRequestFields(BigEndianStructure):
    _fields_ = [
        ('_start_address', c_uint16),
        ('_qty', c_uint16),
    ]
    
    @property
    def _startAddress(self) -> int:
        return self._start_address
    
    @property
    def _quantity(self) -> int:
        return self._qty
    
    def __str__(self):
        return "Start address: {}, Quantity: {}".format(self._startAddress, self._quantity)
    
    
class BaseModbusReadRequestUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusReadRequestFields),
        ('_data', c_uint8 * sizeof(BaseModbusReadRequestFields))
    ]

    @property
    def fields(self) -> BaseModbusReadRequestFields:
        return self._fields
    
    
    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    
    @classmethod
    def fieldsSize(cls):
        return sizeof(cls)
    
    
    def __str__(self):
        return "{}".format(self.fields, self.rawData)
    
    

class ModbusReadRequestFields(BaseModbusReadRequestUnion):
    def __init__(self, start_address : int, quantity : int):
        self.fields._start_address = start_address
        self.fields._qty = quantity
        
    def __str__(self):
        return super().__str__()
    
    

###########################################################################################

class BaseModbusSingleWriteRequestFields(BigEndianStructure):
    _fields_ = [
        ('_address_', c_uint16),
        ('_value_', c_uint16)
    ]
    
    @property
    def _address(self) -> int:
        return self._address_
    
    @property
    def _value(self) -> int:
        return self._value_
    
    def __str__(self):
        return "Address: {}, Value: {}".format(self._address, self._value)
    

class BaseModbusSingleWriteRequestUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusSingleWriteRequestFields),
        ('_data', c_uint8 * sizeof(BaseModbusSingleWriteRequestFields))
    ]
    
    @property
    def fields(self) -> BaseModbusSingleWriteRequestFields:
        return self._fields
    
    
    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    @classmethod
    def fieldsSize(cls):
        return sizeof(cls)

    def __str__(self):
        return "{}".format(self.fields, self.rawData)


class ModbusSingleWriteRequestFields(BaseModbusSingleWriteRequestUnion):
    def __init__(self, address : int, value : int):
        self.fields._address_ = address
        self.fields._value_ = value
        
    def __str__(self):
        return super().__str__()
    
    
###########################################################################################

class BaseModbusMultipleWriteRequestFields(BigEndianStructure):
    _fields_ = [
        ('_address_', c_uint16),
        ('_qty_', c_uint16),
        ('_byte_count_', c_uint16)
    ]
    
    @property
    def _address(self) -> int:
        return self._address_
    
    @property
    def _quantity(self) -> int:
        return self._qty_
    
    @property
    def _byteCount(self) -> int:
        return self._byte_count_
    
    def __str__(self):
        return "Address: {}, Value: {}, Byte Count: {}".format(self._address, self._quantity, self._byteCount)
    
class BaseModbusMultipleWriteRequestUnion(Union):
    _fields_ = [
        ('_fields', BaseModbusMultipleWriteRequestFields),
        ('_data', c_uint8 * sizeof(BaseModbusMultipleWriteRequestFields))
    ]
    
    @property
    def fields(self) -> BaseModbusMultipleWriteRequestFields:
        return self._fields
    
    
    @property
    def rawData(self) -> bytes:
        return bytes(self._data)
    
    @classmethod
    def fieldsSize(cls):
        return sizeof(cls)

    def __str__(self):
        return "{}".format(self.fields, self.rawData)

class ModbusMultipleWriteRequestFields(BaseModbusMultipleWriteRequestUnion):
    def __init__(self, address : int, quantity : int, byte_count : int):
        self.fields._address_ = address
        self.fields._qty_ = quantity
        self.fields._byte_count_ = byte_count
        
    @property
    def address(self):
        return self.fields._address
    
    @property
    def quantity(self):
        return self.fields._quantity
    
    @property
    def byteCount(self):
        return self.fields._byteCount
        
    def __str__(self):
        return super().__str__()


###########################################################################################

