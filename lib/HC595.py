"""
File that contains the classes required for using 595 shift registers with
MicroPython enabled microcontrollers.
There will be a class for the entire shift register and then a subclass for
each pin in the register. This way the the entire shift register can be used
as a true output expander. Each bit or output will then be able to used as a
"stand alone" pin. The classes and methods will then take care of write out
the correct data to the shift register.

Boards the library has been tested on:
WiPy3.0 - P. Cassiman
LoPy4 - P. Cassiman
"""

################################## TODO #######################################


########################### Import statements #################################
from machine import Pin


######################### Variable declarations ###############################
__version__ = 1.0
__author__ = 'P. Cassiman'


######################### Function declarations ###############################


########################### Class declarations ################################


class ShiftRegister:
    """
    Class for controlling 595 shift registers from the 74-series logic IC's.
    The class supports multiple shift registers in series. If more physical
    shift registers are present than declared in code. These extra registers
    will remain blank, as the contents of the shift registers gets cleared
    before each write operation.
    The class supports write operations of the entire shift registers, single
    bytes and individual bits.
    The former two operation are the same when only one shift register is
    connected. But when multiple shift registers have been connected, you can
    write to the entire group and write to all shift registers or you can write
    to a single shift register in the group.
    """

    # attributes for the shift out order, normal is LSB first
    shift_order_reverse = 1
    shift_order_normal = 0

    def __init__(self, SER, SRCLK, RCLK, OE, SRCLR, N_SR=1, order=None):
        """
        Constructor for the shift register class, all that is required is all
        the pins.

        :param SER: The serial input the shift register.

        :param SRCLK: Clock signal for the serial data input.

        :param SRCLR: Clear input for the data, this won't clear the data
                      latched on the output. A low pulse will reset the data.

        :param RCLK: The latch clock for the data, this will place the data
                     from the shift register onto the output.

        :param OE: When this input is high the output will be in 3-state.

        :param N_SR: The number of shift registers have been placed in series.

        :param order: The order in which the bits will be shifted out. Either
                      LSB or MSB first.
        """

        # Storing the relevant pins
        self.SER = ShiftRegister._make_pin(SER, 0)
        self.SRCLK = ShiftRegister._make_pin(SRCLK, 0)
        self.RCLK = ShiftRegister._make_pin(RCLK, 0)
        self.OE = ShiftRegister._make_pin(OE, 0)
        self.SRCLR = ShiftRegister._make_pin(SRCLR, 1)

        # Storing the amount of connected shift registers
        if order > 0:
            self.N_SR = int(N_SR)
        else:
            raise ValueError('Number of shift registers hase to be positive')

        # If no order is given use the default normal order
        if order == None:
            self.order = ShiftRegister.shift_order_normal
        else:
            # If an order is given use that one
            if order == 0 or order == 1:
                self.order = int(order)
            else:
                raise ValueError('Order has to be either 0 or 1')
        # initialise the data attribute to zero
        self.data = 0

    def clear_register(self):
        """
        This method will reset the register to all zero's.
        It uses the register clear pin on the shift register. For data safety
        the outputs are first brought into 3-state.
        After that the reset is asserted. Then the register clock is pulsed to
        bring the zero's onto the output.
        Finally the outputs are taken out of 3-state.
        The data attribute is also set back to 0.
        """

        self.OE.value(1)

        self.SRCLR.value(0)
        self.SRCLR.value(1)

        self.RCLK.value(1)
        self.RCLK.value(0)

        self.OE.value(0)

        self.data = 0

    def read_register(self):
        """
        This function will read the shift register and return the value of the
        register. However since the 595 register do not support reading back
        the stored value, the data attribute is returned instead.
        """

        return self.data

    def read_byte(self, byte=0):
        """
        This function will return a single byte out of the data attribute.
        See docstring of read_register function, for more detail.
        """

        return (self.data >> (8 * byte)) & 0b11111111

    def read_bit(self, bit=0):
        """
        This function will return a single bit out of the data attribute.
        See docstring of read_register function, for more detail.
        """

        return (self.data >> bit) & 0b1

    def write_register(self, data=None):
        """
        Function for shifting out the data to the shift registers. Data can
        either be given to the function or not. When no data is given the data
        attribute of the object is used. Otherwise the data attribute is
        updated. Either case it is the data attribute that is used as a
        reference for shifting out the data.
        All data is shifted out, according to the N_SR attribute, after which
        a pulse is asserted on the latch clock, bringing the data on the
        output.
        """

        if data:
            # When data is given update the data attribute
            # The new data is kept within size of the register
            self.data = data & (2 ** (8 * self.N_SR) - 1)
        else:
            # If no data is given, do nothing
            pass

        self.SRCLR.value(0)
        self.SRCLR.value(1)

        for i in range(8 * self.N_SR):
            # Running through the loop 8 times per shift register
            if self.order == ShiftRegister.shift_order_reverse:
                # If the shift out order is reversed, this algorithm is used
                # to find the bit.
                self.SER.value((self.data >> ((8 * self.N_SR) - i)) % 2)
            else:
                # If the shift out order is not reversed, this algorithm is
                # used for finding the bit.
                self.SER.value((self.data >> i) % 2)
            self.SRCLK.value(1)
            self.SRCLK.value(0)

        self.RCLK.value(1)
        self.RCLK.value(0)

    def write_byte(self, data, byte=0):
        """
        This function will first set a byte in the data attribute and then
        write it out to the output.
        """

        # The data is kept within one byte through the AND operation
        self._set_byte(data & 0b11111111, byte)
        self.write_register()

    def write_bit(self, state, bit=0):
        """
        This function will first set a bit in the data attribute and then
        write it out to the output.
        """

        # The data is kept within one bit through the AND operation
        self._set_bit(state & 0b1, bit)
        self.write_register()

    def _set_byte(self, data, byte=0):
        """
        This function will set a single byte in the data attribute.
        This is useful when multiple shift registers have been connected in
        series. This also enables support for treating each shift register in
        the series as an individual 8-bit port.
        """

        for i in range(8):
            self._set_bit(((data >> i) % 2), (i + (8 * byte)))

    def _set_bit(self, state, bit=0):
        """
        This function will set a single bit in the data attribute. This allows
        control over single outputs on the shift register. These can then also
        be used as single pins. Making the shift register a true output
        expander
        """

        # AND operations for un-setting bits
        self.data &= ~(1 << bit)
        # OR operations for setting bits
        self.data |= (state << bit)

    @staticmethod
    def _make_pin(pin, state):
        if type(pin) == int:
            pin = 'P' + str(pin)
            return Pin(pin, mode=Pin.OUT, value=state)
        elif type(pin) == str:
            return Pin(pin, mode=Pin.OUT, value=state)
        else:
            return pin


class ShiftRegisterPins:
    """
    This class allows to use and control of single output pins on a shift
    register. This makes the shift register a cheap and easy to use output
    expander. However even though only a single bit is changed on the entire
    register. The data is rewritten to the entire register.
    This could make code really slow; if possible it is best to update the
    data of the entire register at once.
    """

    def __init__(self, register, number):
        """
        Constructor for this class
        :param register: The shift register object on which the pin is located
        :param number: The bit number of the pin (zero indexed)
        """

        self.register = register
        self.number = number

    def value(self, state=None):
        """
        docstring
        """

        if state == None:
            return self.register.read_bit(self.number)
        else:
            self.register.write_bit(state, self.number)

    def toggle(self):
        """
        docstring
        """

        state = self.value()
        if state:
            self.off()
        else:
            self.on()

    def off(self):
        """
        docstring
        """

        self.register.write_bit(0, self.number)

    def on(self):
        """
        docstring
        """

        self.register.write_bit(1, self.number)



################################# Main program ################################

if __name__ == '__main__':
    # run some test program
