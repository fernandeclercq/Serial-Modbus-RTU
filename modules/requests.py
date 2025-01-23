
from modules.base.header import ModbusFrameHeader
from modules.base.inner_fields_request import ModbusReadRequestFields, ModbusSingleWriteRequestFields, ModbusMultipleWriteRequestFields
from modules.base.crc import ModbusFrameCRC
from modules.defines import ModbusExceptionCodes, ModbusFunctionCode


class BaseModbusReadRequest:
    
    _MODBUS_FC_ = ModbusFunctionCode.NO_FC
    
    def __init__(self, slave_id : int, address : int, quantity : int):
        self.header : ModbusFrameHeader = ModbusFrameHeader(slave_id, self._MODBUS_FC_)
        self.innerFields : ModbusReadRequestFields = ModbusReadRequestFields(address, quantity)
        self.crc : ModbusFrameCRC = ModbusFrameCRC()
        self.crc.generateCrc(self.payload)
        
        
    @property
    def payload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.innerFields.rawData)
        return buff
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.payload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Inner fields: {}, CRC: {}".format(self.header, self.innerFields, self.crc)


class ModbusReadCoilsRequest(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_COILS
    
    
class ModbusReadDiscreteInputsRequest(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_DISCRETE_INPUTS
    
    
class ModbusReadHoldingRegistersRequest(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_HOLDING_REGISTERS
    
    
class ModbusReadInputRegistersRequest(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_INPUT_REGISTERS
    
        
###################################################################################################################

class BaseModbusSingleWriteRequest:
    _MODBUS_FC_ = ModbusFunctionCode.NO_FC
    
    def __init__(self, slave_id : int, address : int, value : int):
        self.header : ModbusFrameHeader = ModbusFrameHeader(slave_id, self._MODBUS_FC_)
        self.innerFields : ModbusSingleWriteRequestFields = ModbusSingleWriteRequestFields(address, value)
        self.crc : ModbusFrameCRC = ModbusFrameCRC()

        self.crc.generateCrc(self.payload)
        
        
    @property
    def address(self):
        return self.innerFields.fields._address
    
    @property
    def value(self) -> int:
        return self.innerFields.fields._value
    
    @property
    def payload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.innerFields.rawData)
        return buff
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.payload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Inner fields: {}, CRC: {}".format(self.header, self.innerFields, self.crc)
    

class ModbusWriteSingleCoilRequest(BaseModbusSingleWriteRequest):
    _MODBUS_FC_ = ModbusFunctionCode.WRITE_SINGLE_COIL
    
    def __init__(self, slave_id, address, value : bool):
        _final_val : int = 0x0000
        
        if value:
            _final_val = 0xFF00
        
        super().__init__(slave_id, address, _final_val)
        
        
class ModbusWriteSingleRegisterRequest(BaseModbusSingleWriteRequest):
    _MODBUS_FC_ = ModbusFunctionCode.WRITE_SINGLE_HOLDING_REG
    
    
###################################################################################################################

class BaseModbusMultipleWriteRequest:
    _MODBUS_FC_ = ModbusFunctionCode.NO_FC
    
    def __init__(self, slave_id : int, address : int, quantity : int, byte_count : int, values : bytes):
        self.header : ModbusFrameHeader = ModbusFrameHeader(slave_id, self._MODBUS_FC_)
        self.innerFields : ModbusMultipleWriteRequestFields = ModbusMultipleWriteRequestFields(address, quantity, byte_count)
        self._values : bytes | list[int] = values
        
        self.crc : ModbusFrameCRC = ModbusFrameCRC()

        self.crc.generateCrc(self.payload)
        
        
    
    @property
    def slaveId(self) -> int:
        return self.header.slaveAddress
    
    @property
    def address(self) -> int:
        return self.innerFields.address
    
    @property
    def quantity(self) -> int:
        return self.innerFields.quantity
    
    
    @staticmethod
    def formatValues(values : list[int]):
        tmp_array : list[int] = []
        
        for val in values:
            # Cap the values to 0xFFFF
            tmp = val & 0xFFFF
            # Create LSB Byte
            lsb = tmp & 0xFF
            # Create MSB Byte 
            msb = tmp >> 8 & 0xFF
            
            # Append bytes to list
            tmp_array.append(lsb)
            tmp_array.append(msb)
            
        # Save the int array as bytes
        return bytes(tmp_array)
    
    
    @property
    def values(self) -> bytes:
        return self._values
        

    @property
    def payload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.innerFields.rawData)
        buff.extend(self.values[0:self.innerFields.byteCount])
        return buff
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.payload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Inner fields: {}, CRC: {}".format(self.header, self.innerFields, self.crc)
    
    
    
class ModbusWriteHoldingRegistersRequest(BaseModbusMultipleWriteRequest):
    _MODBUS_FC_ = ModbusFunctionCode.WRITE_MULTIPLE_HOLDING_REG
    
    def __init__(self, slave_id : int, address : int, quantity : int, values : bytes):
        
        _final_qty : int = 0
        
        if quantity > 123:
            _final_qty = 123
        else:
            _final_qty = quantity
        
        super().__init__(slave_id, address, _final_qty, (_final_qty * 2), values)
    
    
    
    
###################################################################################################################