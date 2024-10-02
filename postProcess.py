import sys
import os
import subprocess
sys.path.insert(1,'/home/home01/scdrw/scripts/python/processing/run') 

make_video = False
make_image = False
rise_height_calc = False
instability_calc = False

if ( len(sys.argv) == 1 ):
    print('\nNo arguments found, please restart with operation arguments.  Options:')
    print(' 1. image')
    print(' 2. video')
    print(' 3. riseheight\n')

    exit()
else:
    print(' ')
    for i in range(0,len(sys.argv)-1):
        if ( sys.argv[i+1] == 'image' ):
            make_image = True
        elif ( sys.argv[i+1] == 'video' ):
            make_video = True
        elif ( sys.argv[i+1] == 'riseheight' ):
            rise_height_calc = True
        elif ( sys.argv[i+1] == 'instability' ):
            instability_calc = True
        else:
            print(''.join(['Option ',sys.argv[i+1],' no recognised. Continuing with other operations.\n']))

# Filename:
filename = "plume"    # Specify name of files.
filename_len = len(filename) + 3

# Counting number of files in directory.
files = os.listdir(".")
file_count = len([f for f in files if f[:filename_len] == filename + '0.f'])

# Script options.
#make_video = False
#make_image = False
#rise_height_calc = True

class field:
    def __init__(self,name):
        self.name = name
        self.folder = name
        self.set_limits = False
        self.limits = [0.0, 0.0]
        self.scale = -0.5

fields = [ field('vvel') ]
#fields = [ field('vvel'), field('magvel'), field('hvel'), field('th') ]
fields[0].set_limits = True
fields[0].limits = [-0.1, 4.0]

#fields[1].set_lmits = True
#fields[1].limits = [0, 4.0]

#fields[1].folder = 'theta'
#fields[1].set_limits = True
#fields[1].limits = [0.0, 1.0]
#fields[1].scale = -5.0/2.0

# Set import simulation values.
order = 6
numelz = 70

fineness = 4

# Define zooming.
zoom_in = False
zoom_vals = [-10, 10, 10, 50]

scaling = False
Pe = 100

## Make video.
if ( make_video ):
    import make_videos as mv

    start_file = 1
    jump = 20

    mv.video(filename,order,start_file,jump,file_count,numelz,fields,fineness,zoom_in,zoom_vals)

## Make single image.
if ( make_image ):
    import make_videos as mv

    file_number = file_count

    mv.image(filename,order,file_number,numelz,fields,fineness,zoom_in,zoom_vals,scaling,Pe)

## Do rise height calculation.
if ( rise_height_calc ):
    import rise_height as rh

    start_file = 1
    jump = 1

    s_val = 0.9

    rh.find_rise_height(filename,order,start_file,jump,file_count,numelz,s_val)

## Do rise height calculation.
if ( instability_calc ):
    import rise_height as rh

    start_file = 1
    jump = 20

    w0 = 0.4951
    s_val = 0.2 * w0

    rh.find_instability_height(filename,order,start_file,jump,file_count,numelz,s_val)

