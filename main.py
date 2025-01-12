from serial import Serial

from modules.requests import ModbusReadCoils, ModbusReadInputRegisters, ModbusReadHoldingRegisters
from modules.requests import ModbusWriteSingleCoil, ModbusWriteSingleRegister, ModbusWriteHoldingRegisters

from modules.responses import ModbusReadCoilsResponse, ModbusReadHoldingRegisters
        


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
    [ 0x0B, 0x01, 0x02, 0xAC, 0xDB, 0xFB, 0x0D, 
     0x37, 0xBC ]
)

# m = ModbusReadCoils(1, 10, 20)

# print(m)
# print(m.data.hex(' '))

# f = ModbusReadDiscreteInputs(1, 10, 20)
# print(f)
# print(f.data.hex(' '))

# sc = ModbusWriteSingleCoil(1, 10, True)

# print(sc)
# print(sc.data.hex(' '))

# mrs = ModbusWriteHoldingRegisters(1, 10, 130, dummy_data)

# print(mrs)
# print(mrs.data.hex(' '))

res = ModbusReadHoldingRegisters(dummy_data_3)
print(res)
print("has errors?: ", res.hasErrors)
print(res.rawData.hex(' '))


print(res.getRegister(3))