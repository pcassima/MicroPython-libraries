"""
docstring

Boards the library has been tested on:
LoPy4 - P. Cassiman
"""

################################## TODO #######################################
# TODO: write MCP23008 class docstrings
# TODO: write MCP23008_pins class
# TODO: Add support for interupt control
# TODO: Finish single pin methods
# TODO: Allow write method to change pullup configuration when mode=input


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

    def __init__(self, address, baudrate=100000):
        """
        Constructor for the MCP23008 object. This method will save the address
        of the IC and start an I2C object with the given baudrate. For now the
        I2C object can only be made on BUS0 and as a master.
        """
        self.address = address
        self.i2c = I2C(0, I2C.MASTER, baudrate=baudrate)

    def write(self, data):
        """
        Writes the data to the output latches, if the pins are defined as
        inputs, the write method will have no effect. The data will be stored
        in the register, but not appear on the output
        """
        self.i2c.writeto_mem(self.address, MCP23008._OLAT, bytes([data]))

    def read(self):
        """
        Reads the actual value on the in or ouputs. This method works when the
        mode is output or when it is input. This allows for checking on the
        output latches.
        """
        return self.i2c.readfrom_mem(self.address, MCP23008._GPIO, 1)

    def mode(self, mode):
        """
        Sets the mode of the pins; this can either be output, input, or input
        with pullup.
        """
        if mode == MCP23008.PIN_OUTPUT:
            register_mode = 0x00
        elif mode == MCP23008.PIN_INPUT_NOPULLUP:
            register_mode = 0xFF
        elif mode == MCP23008.PIN_INPUT_PULLUP:
            register_mode = 0xFF
            # setting the pullup register
            self.i2c.writeto_mem(self.address, MCP23008._GPPU, bytes([0xFF]))

        self.i2c.writeto_mem(self.address, MCP23008._IODIR,
                             bytes([register_mode]))


    def write_pin(self, pin, state):
        """
        Method writes to a single pin via bitwise operations
        """
        register_state = self.read()
        # pin_state = (register_state >> pin) & 0x1
        register_state &= ~(1 << pin)
        register_state |= (state << pin)
        self.write(register_state)


    def read_pin(self, pin):
        """
        Method reads from a single pin via bitwise operations
        """
        tmp = self.read()
        return (tmp >> pin) & 0x1

    def pin_mode(self, pin, mode):
        """
        Method to set the mode of a single pin.
        """
        register_mode = self.i2c.readfrom_mem(self.address, MCP23008._IODIR, 1)
        register_mode &= ~(1 << pin)
        if mode == MCP23008.PIN_OUTPUT:
            pass
        elif mode == MCP23008.PIN_INPUT_NOPULLUP:
            register_mode |= 1 << pin
            pullup = self.i2c.readfrom_mem(self.address, MCP23008._GPPU, 1)
            pullup &= ~(1 << pin)
            self.i2c.writeto_mem(self.address, MCP23008._GPPU, bytes([pullup]))
        elif mode == MCP23008.PIN_INPUT_PULLUP:
            register_mode |= 1 << pin
            pullup = self.i2c.readfrom_mem(self.address, MCP23008._GPPU, 1)
            pullup |= (1 << pin)
            self.i2c.writeto_mem(self.address, MCP23008._GPPU, bytes([pullup]))
        self.i2c.writeto_mem(self.address, MCP23008._IODIR,
                             bytes([register_mode]))


class MCP23008_pins:
    """
    Class that represents individual pins on the MCP23008's output. Has the
    same interaction as the built-in Pin function from the machine module.
    """

    PIN_OUTPUT = MCP23008.PIN_OUTPUT
    PIN_INPUT_NOPULLUP = MCP23008.PIN_INPUT_NOPULLUP
    PIN_INPUT_PULLUP = MCP23008.PIN_INPUT_PULLUP

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
