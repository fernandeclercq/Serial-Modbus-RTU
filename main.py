from serial import Serial

from modules.requests import ModbusReadCoilsRequest, ModbusReadInputRegistersRequest, ModbusReadHoldingRegistersRequest
from modules.requests import ModbusWriteSingleCoilRequest, ModbusWriteSingleRegisterRequest, ModbusWriteHoldingRegistersRequest

from modules.responses import ModbusReadCoilsResponse, ModbusReadHoldingRegistersResponse, ModbusReadInputRegistersResponse
        


dummy_data : bytes = bytes(list(range(0, 256)))

dummy_data_2 : bytes = bytes(
    [0x0B, 
     0x01,
     0x04,
     0xCD, 0x6B, 
     0xB2, 0x7F, 
     
     0x2B, 0xE1]
)

dummy_data_3 = bytes(
    [ 
     0x0B, 
     0x01, 
     0x02, 
     0xAC, 0xDB, 0xFB, 0x0D, 0xDE, 0xAD,
     0x37, 0xBC ]
)




res = ModbusReadHoldingRegistersResponse(dummy_data_3)
print(res)
print("has errors?: ", res.hasErrors)
print(res.rawData.hex(' '))


print(res.getRegister(0))