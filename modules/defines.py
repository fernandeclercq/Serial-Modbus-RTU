
from modules.generic import BaseLabelEnum

class ModbusExceptionCodes(BaseLabelEnum):
    # Custom Error Codes
    NO_ERROR                        =   0, "No Errors"

    ILLEGAL_FUNCTION                =   1, "Illegal function"
    ILLEGAL_DATA_ADDRESS            =   2, "Illegal Data Address"
    ILLEGAL_DATA_VALUE              =   3, "Illegal Data Value"
    SLAVE_DEVICE_FAILURE            =   4, "Slave Device Failure"
    ACKNOWLEDGE                     =   5, "Acknowledge"
    SLAVE_DEVICE_BUSY               =   6, "Slave Device Busy"
    
    
    # Custom Error Codes
    SERIAL_EMPTY_RECEIVE_BUFFER     =   20, "No Device Response"
    
    # Data Error Codes
    INVALID_CRC                     =   30, "Invalid CRC"
    

class ModbusFunctionCode(BaseLabelEnum):
    
    NO_FC = 0, "No Function Code"
    
    READ_COILS = 1, "Read Coils"
    READ_DISCRETE_INPUTS = 2, "Read Discrete Inputs"
    READ_HOLDING_REGISTERS = 3, "Read Holding Registers"
    READ_INPUT_REGISTERS = 4, "Read Input Registers"
    WRITE_SINGLE_COIL = 5, "Write Single Coil"
    WRITE_SINGLE_HOLDING_REG = 6, "Write Single Holding Register"
    WRITE_MULTIPLE_HOLDING_REG = 0x10, "Write Multiple Holding Registers"
    
    
    ERROR_NO_FC = 128, "Error No Function Code"
    ERROR_READ_COILS = 1 + 128, "Error Read Coils"
    ERROR_READ_DISCRETE_INPUTS = 2 + 128, "Error Read Discrete Inputs"
    ERROR_READ_HOLDING_REGISTERS = 3 + 128, "Error Read Holding Registers"
    ERROR_READ_INPUT_REGISTERS = 4 + 128, "Error Read Input Registers"
    ERROR_WRITE_SINGLE_COIL = 5 + 128, "Error Write Single Coil"
    ERROR_WRITE_SINGLE_HOLDING_REG = 6 + 128, "Error Write Single Holding Register"
    ERROR_WRITE_MULTIPLE_HOLDING_REG = 0x10 + 128, "Error Write Multiple Holding Registers"
    
    
    
    