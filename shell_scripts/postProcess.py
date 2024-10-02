#Link to path in which postProcess_lib is stored.
import sys
import os
import subprocess
print(' ')
# Filename:
filename = "plume"    # Specify name of files.
filename_len = len(filename) + 1

###########################################################
## Script options #########################################
###########################################################
# Choices: 'ke_spectrum', 'nbl', 'rise_height', 'make_video', 'run_checks', 'print_mesh'
script_choices = [ 'make_video' ]
jumps =          [ 20 ] # Number of files to skip.

# Choices for videos.
plot_choices = [ 'vvel' ]

# Start from file.
start_file = 1
# Threshold value for edge determination.
svalue = 0.03
# Number of elements in the z-direction.
numelz = 30
# Order (value of lx1).
order = 8
###########################################################
###########################################################

# Counting number of files in directory.
files = os.listdir(".")
file_count = len([f for f in files if f[:filename_len] == filename + '0'])
#file_count = 2000
print('Number of data files is ' + str(file_count) + '.')

def print_statements(script_name,start_file,jump):

    print('\n\nPerforming ' + script_name + ' calculation...')
    print('------------------------------------------')

    print('Start at file ' + str(start_file) + '.')

#    jump = 5    # Number of files to skip each simulation.
    print('Skip every ' + str(jump) + ' files.')

    # Computes number of calculations to perform.
    to_calculate = int(round(float(file_count)/float(jump) - start_file + 1,0))
    print('Performing ' + str(to_calculate) + ' calculations.')

    return

print('Running with order = ' + str(order) + '.')
print('Running with numelz = ' + str(numelz) + '.')

# Other parameters:
if ( os.path.isfile('plume.rea') ):
    COMMAND1 = "awk '/p137/ { print $1 }' plume.rea > r0.txt"
    COMMAND2 = "rm r0.txt"
    subprocess.call(COMMAND1, shell=True)

    f = open('r0.txt')
    R0 = float(f.readline())

    subprocess.call(COMMAND2, shell=True)

    print('R0 retrieved from plume.rea with value: ' + str(R0) + '.')
else:
    R0 = 0.05
    print('File plume.rea not found.  R0 taken to be: ' + str(R0) + '.')

# Insert path (for comp-pc6076 vs ARC vs VIPER).
#sys.path.insert(1,'/home/cserv1_a/soc_pg/scdrw/Documents/nbudocuments/PhD/SimNumerics/Python/postProcessingLib/scripts')      # Comp-pc6076
sys.path.insert(1,'/home/home01/scdrw/scripts/python/processing/run')          # ARC
#sys.path.insert(1,'/home/617122/Python/scripts')          # VIPER

def ke_spectrum():
        import kinetic_energy as ke
        ke.ke_spectrum(filename,
        start_file,      # Start file
        jump,      # Jump
        file_count,      # Final timestep
        numelz     # Number of elements in z-direction
        )
        return

def riseHeightCalculation():
        import compute_outline as co
        co.riseHeightCalculation(filename,
        order,      # Order 
        3,      # Dimension
        start_file,      # Start file
        jump,      # Jump
        file_count,      # Final timestep
        numelz,     # Number of elements in z-direction
        svalue,   # Cutoff value for s
        0.5,      # start averaging at this time
        0      # Image on/off
        )
        return

def makeVideo():
        import make_videos as mv
        mv.pseudoColour_simple(filename,
        order,      # Order 
        3,      # Dimension
        start_file,      # Start file
        jump,      # Jump
        file_count,      # Final timestep
        numelz,     # Number of elements in z-direction
        plot_choices, # Type of video to make
        set_cvals,
        log_plot,
        zoom_in,
        zoom_vals
        )
        return

def make_image():
        import make_videos as mv
        mv.pseudoColour_singleImage(filename,
        order,      # Order 
        3,      # Dimension
        file_number,      
        numelz,     # Number of elements in z-direction
        plot_choice, # Type of video to make
        set_cvals,
        log_plot,
        zoom_in,
        zoom_vals
        )
        return


def umbrellaOutline():
        import compute_outline as co
        co.umbrellaOutline(filename,
        order,      # Order 
        3,      # Dimension
        start_file,      # Start file
        jump,      # Jump
        file_count,      # Final timestep
        numelz,
        1      # Image on/off
        )
        return

def printMesh():
        import make_videos as mv
        mv.print_mesh(filename,R0)
        return

def runChecks():
        import run_checks as rc
        rc.velocity_inlet_average(filename,
        3,      # Dimension
        start_file,      # Start file
        jump,      # Jump
        file_count,      # Final timestep
        R0,
        plot_choice,
        )
        return

def integrate():
        import integration as inte
        inte.integrate_plume( filename,
        start_file,
        jump,
        file_count,
        numelz
        )


def choose_function(argument):
        switcher = {
                0: ke_spectrum,
                1: riseHeightCalculation,
                2: makeVideo,
                3: printMesh,
                4: runChecks,
                5: umbrellaOutline,
                6: make_image,
                7: integrate,
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument)

        return func()


for j in range(0,len(script_choices)):
   
    script_choice = script_choices[j]
    jump = jumps[j]
    print_statements(script_choice,start_file,jump)

    # Choose script to run.
    if ( script_choice == 'ke_spectrum' ):
        choose_function(0)
    elif ( script_choice == 'rise_height' ):
        print('Running with s-value = ' + str(svalue) + '.')
        choose_function(1)
    elif ( script_choice == 'make_video' ):
        set_cvals = True
        log_plot = False
        zoom_in = True
        zoom_vals = [-50.0, 50.0, 0.0, 400.0]
        for i in range(0,len(plot_choices)):
            plot_choice = plot_choices[i]
            print('\nMaking video of ' + plot_choice+ '...')
        choose_function(2)
    elif ( script_choice == 'make_image' ):
        set_cvals = False
        log_plot = False
        zoom_in = False
        zoom_vals = [-1.0, 1.0, 0.0, 2.0]
        for i in range(0,len(plot_choices)):
            plot_choice = plot_choices[i]
            print('\nMaking ' + plot_choice + ' image of file number ' + str(file_number) + '...')
            choose_function(6)

    elif ( script_choice == 'print_mesh' ):
        choose_function(3)
    elif ( script_choice == 'run_checks' ):
        choose_function(4)
        plot_choice = 'ps'      # choices: ps, vvel, or vorticity
    elif ( script_choice == 'nbl'):
        choose_function(5)
    elif ( script_choice == 'integrate'):
        choose_function(7)
    else:
        print('Error in script_choice.')

