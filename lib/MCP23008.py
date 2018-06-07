"""
docstring

Boards the library has been tested on:
"""

################################## TODO #######################################
# TODO: write MCP23008 class docstrings
# TODO: write MCP23008_pins class
# TODO: Add support for interupt control
# TODO: Finish single pin methods



########################### Import statements #################################
from machine import I2C


######################### Variable declarations ###############################
__version__ = 1.0
__author__ = 'P. Cassiman'


######################### Function declarations ###############################


########################### Class declarations ################################


class MCP23008:
    """
    Class for controlling the MCP23008 IC from Microchip.
    The IC can be controlled as a single 8-bit block (1-byte) or can be used
    to control individual pins separately.
    All internal register addresses have been declared as class attributes.
    Other class attributes can be used to define pin modes and baudrate.
    """

    _IODIR = 0x00
    _IPOL = 0x01
    _GPINTEN = 0x02
    _DEFVAL = 0x03
    _INTCON = 0x04
    _IOCON = 0x05
    _GPPU = 0x06
    _INTF = 0x07
    _INTCAP = 0x08
    _GPIO = 0x09
    _OLAT = 0x0A

    baudrate_100kHz = 100000
    baudrate_400kHz = 400000

    PIN_OUTPUT = 0
    PIN_INPUT_NOPULLUP = 1
    PIN_INPUT_PULLUP = 2

    HIGH = 1
    LOW = 0

    def __init__(self, address, baudrate=100000):
        """
        docstring
        """
        self.address = address
        i2c = I2C(0, I2C.master, baudrate=baudrate)

    def write(self, data):
        """
        docstring
        """
        i2c.writeto_mem(self.address, cls._OLAT, bytes(data))

    def read(self):
        """
        docstring
        """
        return i2c.readfrom_mem(self.address, cls._GPIO, 1)

    def mode(self, mode):
        """
        docstring
        """
        if mode == cls.PIN_OUTPUT:
            register_mode = 0x00
        elif mode == cls.PIN_INPUT_NOPULLUP:
            register_mode = 0xFF
        if mode == cls.PIN_INPUT_PULLUP:
            register_mode = 0xFF
            i2c.writeto_mem(self.address, cls._GPPU, bytes(0xFF))
        i2c.writeto_mem(self.address, cls._IODIR, bytes(register_mode))


    def write_pin(self, pin, state):
        """
        docstring
        """
        register_state = self.read()
        pin_state = (register_state >> pin) & 0x1
        register_state &= ~(1 << pin)
        register_state |= (state << pin)
        self.write(register_state)


    def read_pin(self, pin):
        """
        docstring
        """
        tmp = self.read()
        return (tmp >> pin) & 0x1

    def pin_mode(self, pin, mode):
        """
        docstring
        """
        register_mode = i2c.readfrom_mem(self.address, cls._IODIR, 1)
        register_mode &= ~(1 << pin)
        if mode == cls.PIN_OUTPUT:
            pass
        elif mode == cls.PIN_INPUT_NOPULLUP:
            register_mode |= 1 << pin
            pullup = i2c.readfrom_mem(self.address, cls._GPPU, 1)
            pullup &= ~(1 << pin)
            i2c.writeto_mem(self.address, cls._GPPU, bytes(pullup))
        elif mode == cls.PIN_INPUT_PULLUP:
            register_mode |= 1 << pin
            pullup = i2c.readfrom_mem(self.address, cls._GPPU, 1)
            pullup |= (1 << pin)
            i2c.writeto_mem(self.address, cls._GPPU, bytes(pullup))
        i2c.writeto_mem(self.address, cls._IODIR, bytes(register_mode))


class MCP23008_pins:
    """
    Class that represents individual pins on the MCP23008's output. Has the
    same interaction as the built-in Pin function from the machine module.
    """

    PIN_OUTPUT = MCP23008.PIN_OUTPUT
    PIN_INPUT_NOPULLUP = MCP23008.PIN_INPUT_NOPULLUP
    PIN_INPUT_PULLUP = MCP23008.PIN_INPUT_PULLUP

    HIGH = 1
    LOW = 0

    def __init__(self, IC, number, mode):
        """
        Constructor for a single pin on the MCP23008
        :param IC: The MCP23008 object on which the pin is located.
        :param number: The output number of the pin (0-7).
        :param mode: The mode of the pin; Output, Input or Input with a pullup.
        """

        self.IC = IC
        self.number = number
        self.IC.pin_mode(self.number, mode)

    def value(self, state=None):
        """
        This method will either set the state of the pin or return the current
        state. If no value is given for the state, the method will return the
        current state of the pin.
        If a value is given, the method will set the pin accordingly.
        :param state: The state to which the pin has to be set.
        """

        if state == None:
            return self.IC.read_pin(self.number)
        else:
            self.IC.write_pin(self.number, state)

    def toggle(self):
        """
        This method will toggle the state of the pin. If the current state is
        on the function will turn off the pin and vice versa.
        """

        state = self.value()
        if state:
            self.off()
        else:
            self.on()

    def off(self):
        """
        Turns off the pin.
        """

        self.IC.write_pin(self.number, 0)

    def on(self):
        """
        Turns on the pin.
        """

        self.IC.write_pin(self.number, 1)


################################# Main program ################################
