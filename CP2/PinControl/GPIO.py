import board
import digitalio

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = False