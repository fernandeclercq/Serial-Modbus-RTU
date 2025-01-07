
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


class ModbusReadCoils(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_COILS
    
    
class ModbusReadDiscreteInputs(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_DISCRETE_INPUTS
    
    
class ModbusReadHoldingRegisters(BaseModbusReadRequest):
    _MODBUS_FC_ = ModbusFunctionCode.READ_HOLDING_REGISTERS
    
    
class ModbusReadInputRegisters(BaseModbusReadRequest):
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
    

class ModbusWriteSingleCoil(BaseModbusSingleWriteRequest):
    _MODBUS_FC_ = ModbusFunctionCode.WRITE_SINGLE_COIL
    
    def __init__(self, slave_id, address, value : bool):
        _final_val : int = 0x0000
        
        if value:
            _final_val = 0xFF00
        
        super().__init__(slave_id, address, _final_val)
        
        
class ModbusWriteSingleRegister(BaseModbusSingleWriteRequest):
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
    def payload(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.header.rawData)
        buff.extend(self.innerFields.rawData)
        buff.extend(self._values[0:self.innerFields.byteCount])
        return buff
    
    @property
    def data(self) -> bytes:
        buff : bytearray = bytearray()
        buff.extend(self.payload)
        buff.extend(self.crc.data)
        return buff
    
    def __str__(self):
        return "Header: {}, Inner fields: {}, CRC: {}".format(self.header, self.innerFields, self.crc)
    
    
    
class ModbusWriteHoldingRegisters(BaseModbusMultipleWriteRequest):
    _MODBUS_FC_ = ModbusFunctionCode.WRITE_MULTIPLE_HOLDING_REG
    
    def __init__(self, slave_id, address, quantity, values):
        
        _final_qty : int = 0
        
        if quantity > 123:
            _final_qty = 123
        
        super().__init__(slave_id, address, _final_qty, (_final_qty * 2), values)
    
    
    
    
###################################################################################################################