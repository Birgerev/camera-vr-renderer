from picamera import mmalobj as mo, mmal
from picamera import PiCamera
from time import sleep
from signal import pause
#import time

##-- SETTINGS --##
screen_width = 800
screen_height = 480
y_offset = 50

width_half = int(screen_width/2)

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


#Set camera formats
camera.outputs[0].framerate=60
camera.outputs[0].framesize=(1080,1080)
camera.outputs[0].commit()

#Prepare displayregion
display_region = render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]
display_region.set = mmal.MMAL_DISPLAY_SET_FULLSCREEN | mmal.MMAL_DISPLAY_SET_DEST_RECT
display_region.fullscreen = False

#Map renderers on screen space
#rect format: (minX, minY, width, height)
display_region.dest_rect = mmal.MMAL_RECT_T(0, y_offset, width_half, screen_height)
render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=display_region

display_region.dest_rect = mmal.MMAL_RECT_T(width_half, y_offset, width_half, screen_height)
render_right.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=display_region

#Connect both renderers to sources
splitter.connect(camera.outputs[0])
render_left.connect(splitter.outputs[0])
render_right.connect(splitter.outputs[1])

#Enable Renderers
splitter.enable()
render_left.enable()
render_right.enable()

#Continue rendering unil interrupted
pause()
