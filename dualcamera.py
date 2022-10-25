from picamera import mmalobj as mo, mmal
from picamera import PiCamera

from time import sleep

from signal import pause
import time

camera = mo.MMALCamera()
splitter = mo.MMALSplitter()
render_left = mo.MMALRenderer()
render_right = mo.MMALRenderer()

#camera.control.params[mmal.MMAL_PARAMETER_BRIGHTNESS] = .625
#camera.control.params[mmal.MMAL_PARAMETER_ISO]=800
#color effects?
#mp = camera.control.params[mmal.MMAL_PARAMETER_COLOUR_EFFECT]
#mmal.MMAL_PARAM_IMAGEFX_COLOURPOINT = 0
#clp = mmal.MMAL_PARAM_IMAGEFX_COLOURPOINT
#camera.image_effect = clp
#mp.u = 32768
#mp.v = 65536

#what is printed?
#print(mp.u)

#TODO remove
count=0
lastbuttonstate=0;
presscount=1;

#???
camera.outputs[0].framerate=70
camera.outputs[0].framesize=(1080,720)
camera.outputs[0].commit()

p = render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]
p.set = mmal.MMAL_DISPLAY_SET_FULLSCREEN | mmal.MMAL_DISPLAY_SET_DEST_RECT
p.fullscreen = False

p.dest_rect = mmal.MMAL_RECT_T(0,35,400,480)
render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=p
p.dest_rect = mmal.MMAL_RECT_T(400,35,400,480)
render_right.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=p

splitter.connect(camera.outputs[0])
render_left.connect(splitter.outputs[0])
render_right.connect(splitter.outputs[1])

splitter.enable()
render_left.enable()
render_right.enable()

pause()