from modules.modbus_rtu import ModbusRTU
import time



controller_1 = ModbusRTU("/dev/ttyUSB1", 921600, 0.1)
flip : bool = False

while True:
    
    
    if flip:
        flip = False
        
        controller_1.writeSingleHoldingRegister(0, 0, 1)

        controller_1.writeSingleCoil(0, 2, True)
        
    else:
        flip = True
        controller_1.writeSingleHoldingRegister(0, 0, 2)

        controller_1.writeSingleCoil(0, 2, True)
        
    time.sleep(2)



