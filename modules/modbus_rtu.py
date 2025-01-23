from serial import Serial
from serial import SerialException
import time

from modules.requests import ModbusReadCoilsRequest, ModbusReadInputRegistersRequest, ModbusReadHoldingRegistersRequest
from modules.requests import ModbusWriteSingleCoilRequest, ModbusWriteSingleRegisterRequest, ModbusWriteHoldingRegistersRequest

from modules.responses import ModbusReadCoilsResponse, ModbusReadHoldingRegistersResponse, ModbusReadInputRegistersResponse
from modules.responses import ModbusWriteSingleRegisterResponse, ModbusWriteSingleCoilResponse, ModbusWriteHoldingRegistersResponse
        




class ModbusRTU:
    def __init__(self, port: str, baudrate : str, timeout : float | None = None):
        
        self._timeout : float = timeout
        self._serial : Serial = Serial(port=port, baudrate=baudrate, timeout=timeout)
            

    @property
    def serialConnection(self) -> Serial:
        return self._serial
        
        
    def readCoils(self, slave_id : int, address: int, qty_coils : int) -> ModbusReadCoilsResponse:
        request : ModbusReadCoilsRequest = ModbusReadCoilsRequest(slave_id, address, qty_coils)
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusReadCoilsResponse = ModbusReadCoilsResponse(incoming_bytes)
        
        return response


    def readHoldingRegisters(self, slave_id : int, address : int, quantity : int) -> ModbusReadHoldingRegistersResponse:
        request : ModbusReadHoldingRegistersRequest = ModbusReadHoldingRegistersRequest(slave_id, address, quantity)
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusReadHoldingRegistersResponse = ModbusReadHoldingRegistersResponse(incoming_bytes)
        
        return response
    
    
    def readInputRegisters(self, slave_id : int, address : int, quantity : int) -> ModbusReadInputRegistersResponse:
        request : ModbusReadInputRegistersRequest = ModbusReadInputRegistersRequest(slave_id, address, quantity)
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusReadInputRegistersResponse = ModbusReadInputRegistersResponse(incoming_bytes)
        
        return response
        

    def writeSingleCoil(self, slave_id : int, address : int, value : bool) -> ModbusWriteSingleCoilResponse:
        request : ModbusWriteSingleCoilRequest = ModbusWriteSingleCoilRequest(slave_id, address, value)
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusWriteSingleCoilResponse = ModbusWriteSingleCoilResponse(request)
        
        return response
    
    
    def writeSingleHoldingRegister(self, slave_id : int, address : int, value : int) -> ModbusWriteSingleRegisterResponse:
        request : ModbusWriteSingleRegisterRequest = ModbusWriteSingleRegisterRequest(slave_id, address, value)
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusWriteSingleRegisterResponse = ModbusWriteSingleRegisterResponse(request)
        
        return response
    
    
    def writeMultipleHoldingRegisters(self, slave_id : int, address : int, quantity : int, values : bytes) -> ModbusWriteHoldingRegistersResponse:
        request : ModbusWriteHoldingRegistersRequest = ModbusWriteHoldingRegistersRequest(slave_id, address, quantity, values)
        
        
        self._serial.flush()
        self._serial.write(request.data)
        
        time.sleep(self._timeout)
        
        incoming_bytes = self._serial.read_all()
        
        response : ModbusWriteHoldingRegistersResponse = ModbusWriteHoldingRegistersResponse(request)
        
        return response