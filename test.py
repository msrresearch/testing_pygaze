from pygaze import eyetracker, libscreen, libtime, libinput
from constants import *

display = libscreen.Display()
screen = libscreen.Screen()

keyboard = libinput.Keyboard()

tracker = eyetracker.EyeTracker(display)
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

while True:
	info_text = 'pos: {:>15} | 3D eye position: {:<20}'.format(tracker.sample(),tracker.eye_position_3d())
	screen.clear()
	screen.draw_text(info_text,'black')
	display.fill(screen)
	display.show()
	print(info_text)
	libtime.pause(1000)



print('test')
