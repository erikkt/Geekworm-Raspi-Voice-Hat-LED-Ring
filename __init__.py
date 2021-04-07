# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler

from apa102_pi.colorschemes import colorschemes
from apa102_pi.driver import apa102

NUM_LED = 12
MOSI = 23  # Hardware SPI uses BCM 10 & 11. Change these values for bit bang mode
SCLK = 24  # e.g. MOSI = 23, SCLK = 24 for Pimoroni Phat Beat or Blinkt!


class Geekworm_LED_ring(MycroftSkill):

	def __init__(self):
		super(Geekworm_LED_ring, self).__init__(name="Geekworm_LED_ring")
		
	def initialize(self):
		self.log.info("Pixel Ring: Initializing")
		self.enable()
		self.think = False
		self.think_run = False

	def enable(self):
		self.log.info("Pixel Ring: Enabling")

		self.add_event('recognizer_loop:wakeword',
				self.handle_listener_wakeup)
		self.add_event('recognizer_loop:record_end',
				self.handle_listener_off)

		self.add_event('mycroft.skill.handler.start',
				self.handle_listener_think)
		self.add_event('mycroft.skill.handler.complete',
				self.handle_listener_off)

		self.add_event('recognizer_loop:audio_output_start',
				self.handler_listener_speak)
		self.add_event('recognizer_loop:audio_output_end',
				self.handle_listener_off)

		self.led = apa102.APA102(num_led=NUM_LED, order='rgb', mosi=MOSI, sclk=SCLK)
		self.led.clear_strip()
		self.led.set_global_brightness(11)

	def disable(self):
		self.log.info("Pixel Ring: Disabling")
		self.remove_event('recognizer_loop:wakeup')
		self.remove_event('recognizer_loop:record_end')
		self.remove_event('recognizer_loop:audio_output_start')
		self.remove_event('recognizer_loop:audio_output_end')
		self.remove_event('mycroft.skill.handler.start')
		self.remove_event('mycroft.skill.handler.complete')

	def shutdown(self):
		self.log.info("Pixel Ring: Shutdown")
		self.led.cleanup(led)

	def handle_listener_wakeup(self, message):
		self.log.info("Pixel Ring: Wakeup")
		self.think = True
		#self.think_run = False
		for self.x in range(12):
			self.led.set_pixel_rgb(self.x, 0x00FF00)
		self.led.show()
		
	def handle_listener_off(self, message):
		self.log.info("Pixel Ring: Off")
		if not self.think_run:
			#self.think = False
			self.led.clear_strip()
			for self.x in range(12):
				self.think_run = True
				if not self.think:
					self.think_run = False
					break
				self.led.set_pixel_rgb(self.x, 0x000000)
				if self.x == 11 :
					self.x = -1
				self.led.set_pixel_rgb(self.x+1, 0xFF0000)
				self.led.set_pixel_rgb(self.x+2, 0x0000FF)
				self.led.set_pixel_rgb(self.x+3, 0x00FF00)
				self.led.show()
				time.sleep(0.03)
				
		#self.think = True
		if not self.think_run:
			self.led.clear_strip()

	def handle_listener_think(self, message):
		self.log.info("Pixel Ring: Think")
#		self.led.clear_strip()
#		self.think = False
		
#		if not self.think_run:
#			for self.x in range(12):
#				self.think_run = True
#				if self.think == True:
#					break
#				self.led.set_pixel_rgb(self.x, 0x000000)
#				if self.x == 11 :
#					self.x = -1
#				self.led.set_pixel_rgb(self.x+1, 0xFF0000)
#				self.led.set_pixel_rgb(self.x+2, 0x0000FF)
#				self.led.set_pixel_rgb(self.x+3, 0x00FF00)
#				self.led.show()
#				time.sleep(0.03)


	def handler_listener_speak(self, message):
		self.log.info("Pixel Ring: Speak")
		self.think = False
		#self.think_run = False
		self.led.clear_strip()
		for self.x in range(12):
			self.led.set_pixel_rgb(self.x, 0x0000FF)
		self.led.show()

	@intent_handler(IntentBuilder("").require("EnablePixelRing"))
	def handle_enable_pixel_ring_intent(self, message):
		self.enable()
		self.speak_dialog("EnablePixelRing")

	@intent_handler(IntentBuilder("").require("DisablePixelRing"))
	def handle_disable_pixel_ring_intent(self, message):
		self.disable()
		self.speak_dialog("DisablePixelRing")

def create_skill():
	return Geekworm_LED_ring()
