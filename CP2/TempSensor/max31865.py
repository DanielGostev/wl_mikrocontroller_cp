# SPDX-License-Identifier: MIT

# Simple demo of the MAX31865 thermocouple amplifier.
# Will print the temperature every second.
import time
import board
import busio
import digitalio
import adafruit_max31865



# Create sensor object, communicating over the board's default SPI bus
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP0)
cs = digitalio.DigitalInOut(board.GP1)
cs.direction = digitalio.Direction.OUTPUT # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=4)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
# sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=2)

# Main loop to print the temperature every second.
