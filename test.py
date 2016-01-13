from pygaze import eyetracker, libscreen, libtime, libinput
from constants import *

import threading

display = libscreen.Display()
screen = libscreen.Screen()

keyboard = libinput.Keyboard()

tracker = eyetracker.EyeTracker(display)

print(tracker.spdtresh)
print(tracker.accthresh)
print(tracker.eventdetection)

screen.draw_text('calibrate? [y,n]','red')
display.fill(screen)
display.show()
key,time = keyboard.get_key(['y','n'],None)
print(key)
if key == 'y':
	tracker.calibrate()
else:
	tracker.pxfixtresh = 60.

tracker.start_recording()

class Blink_Detector(threading.Thread):
	def __init__(self, tracker, name='Blink_Detector'):
		super(Blink_Detector,self).__init__(name=name)
		self.tracker = tracker
		self.daemon = True
		self.blink_start = 0.
		self.blink_end = 0.
		self.blink_dur = 0.
	
	def run(self):
		while True:
			self.blink_start = self.tracker.wait_for_blink_start()
			self.blink_end = self.tracker.wait_for_blink_end()
			self.blink_dur = self.blink_end - self.blink_start

bd = Blink_Detector(tracker)
bd.start()


while True:
	pos = tracker.sample()
	info_text = 'pos: {:>15}'.format(pos)
	try:
		gaze_vector = tracker.gaze_vector()
		info_text += '\neye position: {:<60}'.format(tracker.eye_position_3d())
		info_text += '\n3D gaze vector: {:<90}'.format(gaze_vector)
	except AttributeError:
		info_text += '\neye position: NOT SUPPORTED!'
		info_text += '\n3D gaze vector: NOT SUPPORTED!'
	info_text += '\npupil size: {:>15}'.format(tracker.pupil_size())
	info_text += '\nblink_start: {:>15} | blink_end: {:>15} | blink_dur: {:>15}'.format(bd.blink_start,bd.blink_end,bd.blink_dur)
	screen.clear()
	screen.draw_text(info_text,'black')
	screen.draw_fixation(colour='red',pos=pos)
	display.fill(screen)
	display.show()
	print(info_text)
	libtime.pause(10)
