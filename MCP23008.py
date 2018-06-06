"""
docstring
"""
################################## TODO #######################################
# TODO: write MCP23008 class
# TODO: write MCP23008_pins class
# TODO: figure out which methods the classes require


########################### Import statements #################################


######################### Variable declarations ###############################


######################### Function declarations ###############################


########################### Class declarations ################################


class MCP23008:
    """
    docstring
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

    def __init__(self, address):
        """
        docstring
        """

    def write(self, data):
        """
        docstring
        """

    def read(self):
        """
        docstring
        """

    def write_pin(self, pin, data):
        """
        docstring
        """

    def read_pin(self, pin):
        """
        docstring
        """

    def pin_mode(self, pin, mode, pullup):
        """
        docstring
        """

    def pin_polarity(self, pin, polarity):
        """
        docstring
        """


class MCP23008_pins:
    """
    docstring
    """

    def __init__(self, IC):



################################# Main program ################################
