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


class MCP23017_pins:
    """
    Class that represents individual pins on the MCP23017's output. Has the
    same interaction as the built-in Pin function from the machine module.
    """

    def __init__(self, IC, number):
        """
        docstring
        """

    def value(self, state=None):
        """
        docstring
        """

    def toggle(self):
        """
        docstring
        """

    def off(self):
        """
        docstring
        """

    def on(self):
        """
        docstring
        """


################################# Main program ################################
