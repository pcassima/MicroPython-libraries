"""
docstring

Boards the library has been tested on:
"""

################################## TODO #######################################
# TODO: write MCP23017 class
# TODO: write MCP23017_pins class
# TODO: figure out which methods the classes require


########################### Import statements #################################
from machine import I2C


######################### Variable declarations ###############################
__version__ = 0.0
__author__ = 'P. Cassiman'


######################### Function declarations ###############################


########################### Class declarations ################################


class MCP23017:
    """
    Class for controlling the MCP23017 IO-expander.
    """

    # A-bank
    _IODIRA = 0x00
    _IPOLA = 0x01
    _GPINTENA = 0x02
    _DEFVALA = 0x03
    _INTCONA = 0x04
    _IOCONA = 0x05
    _GPPUA = 0x06
    _INTFA = 0x07
    _INTCAPA = 0x08
    _GPIOA = 0x09
    _OLATA = 0x0A

    # B-bank
    _IODIRB = 0x10
    _IPOLB = 0x11
    _GPINTENB = 0x12
    _DEFVALB = 0x13
    _INTCONB = 0x14
    _IOCONB = 0x15
    _GPPUB = 0x16
    _INTFB = 0x17
    _INTCAPB = 0x18
    _GPIOB = 0x19
    _OLATB = 0x1A

    baudrate_100kHz = 100000
    baudrate_400kHz = 400000

    PIN_OUTPUT = 0
    PIN_INPUT_NOPULLUP = 1
    PIN_INPUT_PULLUP = 2


    def __init__(self, address, baudrate=100000):
        """
        Constructor for the MCP23017 object
        param: address: The I2C address of the IO-expander
        param: baudrate: The frequency at which to communicate with the IC
        """
        self.address = address
        self.i2c = I2C(0, I2C.MASTER, baudrate=baudrate)

    def write(self, bank, data):
        """
        Function for writing a byte to a single bank to the MCP23017
        param: bank: Which IO-bank to write the data to (0 or 1).
        param: data: A byte which has to be written to the IO-bank
        """
        self.i2c.writeto_mem(self.address, [bank], bytes([data]))

    def read(self, bank):
        """
        Function for reading the actual value of the pins of one bank.
        param: bank: which bank to read the data from
        return: a byte representing the values on the IO-bank
        """
        return self.i2c.readfrom_mem(self.address, [bank], 1)[0]

    def mode(self, bank, mode):
        """
        Function for setting the mode of an entire bank.
        param: bank: which IO-bank to set the mode of
        param: mode: what mode the bank needs to be set to.
        """

    def write_pin(self, bank, pin, state):
        """
        Function for setting the state if a single pin.
        """
        raise NotImplementedError

    def read_pin(self, bank, pin):
        """
        Function for reading a single pin.
        """
        raise NotImplementedError

    def pin_mode(self, bank, pin, mode):
        """
        Function for setting the mode of a single pin.
        """
        raise NotImplementedError


class MCP23017_pins:
    """
    Class that represents individual pins on the MCP23017's output. Has the
    same interaction as the built-in Pin function from the machine module.
    """

    def __init__(self, IC, number):
        """
        docstring
        """
        raise NotImplementedError

    def value(self, state=None):
        """
        docstring
        """
        raise NotImplementedError

    def toggle(self):
        """
        docstring
        """
        raise NotImplementedError

    def off(self):
        """
        docstring
        """
        raise NotImplementedError

    def on(self):
        """
        docstring
        """
        raise NotImplementedError


################################# Main program ################################

if __name__ == '__main__':
    # run some test program
