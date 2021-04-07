from apa102_pi.colorschemes import colorschemes
from apa102_pi.driver import apa102
import time

NUM_LED = 12
MOSI = 23  # Hardware SPI uses BCM 10 & 11. Change these values for bit bang mode
SCLK = 24  # e.g. MOSI = 23, SCLK = 24 for Pimoroni Phat Beat or Blinkt!


led = apa102.APA102(num_led=NUM_LED, order='rbg', mosi=MOSI, sclk=SCLK)
led.set_global_brightness(11)
led.clear_strip()
stop = False
#for x in range(12):
#        led.set_pixel_rgb(x, 0x00FF00)

led.show()

while not stop:
    for x in range(12):
        led.set_pixel_rgb(x, 0x000000)
        if x == 11 :
            x = -1
        led.set_pixel_rgb(x+1, 0xFF0000)
        led.set_pixel_rgb(x+2, 0x0000FF)
        led.set_pixel_rgb(x+3, 0x00FF00)
        led.show()
        time.sleep(0.03)


time.sleep(5)
stop = True
