# ported to CircuitPython 3.0.0-beta0 by Gregory P. Smith

##
 #  @filename   :   epdif.py
 #  @brief      :   EPD hardware interface implements (GPIO, SPI)
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 4 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #

import adafruit_bus_device.spi_device
import board
import digitalio

# Pin definitions
RST_PIN = board.GP12
BUSY_PIN = board.GP13
DC_PIN = board.GP8
CS_PIN = board.GP9
SPI_MOSI = board.GP11
SPI_CLK = board.GP10
SPI_BUS = None
_init = False


def spi_transfer(data):
    with SPI_BUS as device:
        device.write(data)

def epd_io_bus_init():
    global _init
    if _init:
        raise RuntimeError("epd_io_bus_init() called twice")
    _init = True
    global RST_PIN, DC_PIN, CS_PIN, BUSY_PIN
    DInOut = digitalio.DigitalInOut
    OUTPUT = digitalio.Direction.OUTPUT
    INPUT = digitalio.Direction.INPUT
    RST_PIN = DInOut(RST_PIN)
    RST_PIN.direction = OUTPUT
    DC_PIN = DInOut(DC_PIN)
    DC_PIN.direction = OUTPUT
    CS_PIN = DInOut(CS_PIN)
    CS_PIN.direction = OUTPUT
    BUSY_PIN = DInOut(BUSY_PIN)
    BUSY_PIN.direction = INPUT
    global SPI_BUS
    # bus vs bitbang isn't really important for slow displays, detecting
    # when to use one vs the other is overkill...
    if (SPI_CLK == getattr(board, 'SCK', None) and
        SPI_MOSI == getattr(board, 'MOSI', None)):
        import busio as io_module
    else:
        import bitbangio as io_module
    SPI_BUS = adafruit_bus_device.spi_device.SPIDevice(
            io_module.SPI(SPI_CLK, SPI_MOSI), CS_PIN,
            baudrate=2000000)

### END OF FILE ###