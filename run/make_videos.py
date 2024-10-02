import numpy as np
import math
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as plt_c
from mpl_toolkits.axes_grid1 import make_axes_locatable
# The following allows the script to work over SSH.  Check it still works when not SSH tunnelling.
plt.switch_backend('agg')
import os
import scipy.interpolate as si
from collections import OrderedDict

# Import user-defined modules .
sys.path.insert(1,'/home/home01/scdrw/scripts/python/processing/run/tools')          # ARC
import readingNek as rn
import general as gn

# Print whole arrays instead of truncating.
np.set_printoptions(threshold=sys.maxsize)

def video( filename, order, start_file, jump, final_timestep, numelz, fields, fineness, set_zoom, zoom_vals ):

    plot_colourbar = 'yes'
    order = order - 1

    final_file = int(final_timestep/jump)
    range_vals = [x-(jump-1) for x in np.array(range(1,final_file+1))*jump]

    # Create directories for saving.
    nfields = len(fields)
    save_dir_stub = './processing/images/'
    gn.create_folders( fields, nfields, save_dir_stub, set_zoom )

    # Custom colour map.
    f = open('/home/home01/scdrw/scripts/python/processing/colour_map/full_colour_map.txt','r')
    cm_str = f.read(); cm_str = cm_str[:-1]
    cm_str = [x.split(',') for x in cm_str.split('\n')]
    cm = [[float(v)/256.0 for v in r ] for r in cm_str]
    f.close()

    cm = plt_c.ListedColormap(np.flipud(cm))

    # Reading in mesh data.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename,'0.f00001']))
    Xplane,Zplane,xzplane,coords1,coords2,xi,zi,xlen,zlen,minmax,nel,gll = gn.read_mesh( data, fineness, numelz, set_zoom, zoom_vals )

    minx = minmax[0]
    maxx = minmax[1]
    minz = minmax[2]
    maxz = minmax[3]

    start_threshold = (start_file - 1)*jump
    file_counter = 0

    for k in range_vals:

        file_counter += 1 
        
        if ( k > start_threshold ):

            file_num = int((k-1)/jump + 1)

            # Outputs counter to terminal.
            files_remaining = int(final_file - k/jump + 1)
            sys.stdout.write("\r")
#            sys.stdout.write("Files remaining: {:3d}".format(files_remaining))
            sys.stdout.write("Working on file: ({:3d}/{:3d})...".format(file_num,int(range_vals[-1]/jump)))
            sys.stdout.flush()

            # Reads data files.
            data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename, \
                '0.f',repr(k).zfill(5)]))

            # Run through all plot choices.
            for i in range(0,nfields):

                # Names
                name = fields[i].folder
                if (set_zoom): name = name + "_zoom"
                save_name = ''.join([save_dir_stub,name,'/',name])

                num = 0; S = np.zeros((nel,gll,1))
                if ( fields[i].name == 'vvel' ): S[:,:,0] = np.array(data[:,:,w_i])
                elif ( fields[i].name == 'hvel' ): S[:,:,0] = np.array(data[:,:,u_i])
                elif ( fields[i].name == 'ps' ): S[:,:,0] = np.array(data[:,:,s_i])
                elif ( fields[i].name == 'th' ): S[:,:,0] = np.array(data[:,:,t_i])
                elif ( fields[i].name == 'vorticity' ):
                    S = np.zeros((nel,gll,3))
                    S[:,:,0] = np.array(data[:,:,u_i])
                    S[:,:,1] = np.array(data[:,:,v_i])
                    S[:,:,2] = np.array(data[:,:,w_i])

                arrlength = np.shape(Xplane)
                arrlength = arrlength[0]

                Non,Non,numS = np.shape(S)
                
                Splane = np.zeros((arrlength,numS))

                for num in range(0,numS):
                    Splane[:,num] = np.array(S[coords1,coords2,num])

                Si = np.zeros((zlen,xlen,numS))
                for num in range(0,numS):
                    Si[:,:,num] = si.griddata(xzplane,Splane[:,num],(xi,zi),method='cubic')

                #if (plot_choice == 'th' ):
                #    S_min = 2.0
                #    Si = np.clip(Si,0,S_min)

                # Replace NaNs in values that are outside the domain as zeros.
                where_are_NaNs = np.isnan(Si[:,:,num])
                Si[where_are_NaNs,num] = 0

                #if (log_plot):
                #    Si = np.where(Si<0,0,Si)
                #    Si = np.log([x + 0.001 for x in Si])
                    
                x_size = maxx - minx
                z_size = maxz - minz

                fig_x = 15
                #fig_z = fig_x*(z_size/x_size)
                fig_x = 20
                fig_z = 40

                plt.figure(figsize=(fig_x,fig_z))

                font = {'family' : 'sans',
                        'weight' : 'normal',
                        'size'   : 24}

                plt.rc('font', **font)


    #...........Plotting, decides whether to set c-values.
                if (fields[i].set_limits):
                    lims = fields[i].limits
                    plt.pcolor(xi,zi,Si[:,:,num],cmap=cm,vmin=lims[0],vmax=lims[1])
                else:
                    plt.pcolor(xi,zi,Si[:,:,num],cmap=cm)

                if (plot_colourbar == 'yes' ):
                    cbar = plt.colorbar()
                    plt.draw()

                plt.title("Time: {:3.3f}".format(time))
                plt.axis([minx, maxx, minz, maxz])

                font = {'family' : 'sans',
                        'weight' : 'normal',
                        'size'   : 24}

                plt.rc('font', **font)

                plt.savefig(os.path.join(''.join([save_name,repr(file_counter).zfill(5),'.png'])),bbox_inches='tight')
                plt.close('all') 

    return

def image( filename,order,file_number,numelz,fields,fineness,set_zoom,zoom_vals,scaling,Pe ):

    plot_colourbar = True
    order = order - 1

    # Create directories for saving.
    nfields = len(fields)
    save_dir_stub = './processing/single_images/'
    gn.create_folders( fields, nfields, save_dir_stub, set_zoom )

    # Custom colour map.
    f = open('/home/home01/scdrw/scripts/python/processing/colour_map/full_colour_map.txt','r')
    cm_str = f.read(); cm_str = cm_str[:-1]
    cm_str = [x.split(',') for x in cm_str.split('\n')]
    cm = [[float(v)/256.0 for v in r ] for r in cm_str]
    f.close()

    cm = plt_c.ListedColormap(np.flipud(cm))

    # Reading in mesh data.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename,'0.f00001']))
    Xplane,Zplane,xzplane,coords1,coords2,xi,zi,xlen,zlen,minmax,nel,gll = gn.read_mesh( data, fineness, numelz, set_zoom, zoom_vals )

    minx = minmax[0]
    maxx = minmax[1]
    minz = minmax[2]
    maxz = minmax[3]

    # Scaling.
    if (scaling):
        xi = Pe**(3.0/2.0) * xi
        zi = Pe**(3.0/2.0) * zi
        Xplane = Pe**(3.0/2.0) * Xplane
        Zplane = Pe**(3.0/2.0) * Zplane
        xzplane = Pe**(3.0/2.0) * xzplane

        minx = Pe**(3.0/2.0) * minx
        maxx = Pe**(3.0/2.0) * maxx
        minz = Pe**(3.0/2.0) * minz
        maxz = Pe**(3.0/2.0) * maxz


    # Reading in data to plot.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename, \
        '0.f',repr(file_number).zfill(5)]))

    arrlength = np.shape(Xplane)
    arrlength = arrlength[0]

    # Run through all plot choices.
    for i in range(0,nfields):

        # Names
        name = fields[i].folder
        if (set_zoom): name = name + "_zoom"
        save_name = ''.join([save_dir_stub,name,'/',name])

        num = 0; S = np.zeros((nel,gll,1))
        if ( fields[i].name == 'vvel' ): S[:,:,0] = np.array(data[:,:,w_i])
        elif ( fields[i].name == 'hvel' ): S[:,:,0] = np.array(data[:,:,u_i])
        elif ( fields[i].name == 'ps' ): S[:,:,0] = np.array(data[:,:,s_i])
        elif ( fields[i].name == 'th' ): S[:,:,0] = np.array(data[:,:,t_i])
        elif ( fields[i].name == 'vorticity' ):
            S = np.zeros((nel,gll,3))
            S[:,:,0] = np.array(data[:,:,u_i])
            S[:,:,1] = np.array(data[:,:,v_i])
            S[:,:,2] = np.array(data[:,:,w_i])
        elif ( fields[i].name == 'magvel' ):
            S[:,:,0] = np.sqrt(np.square(np.array(data[:,:,w_i])) + np.square(np.array(data[:,:,u_i])) + np.square(np.array(data[:,:,v_i])))

        Non,Non,numS = np.shape(S)
        Splane = np.zeros((arrlength,numS))

        for num in range(0,numS):
            Splane[:,num] = np.array(S[coords1,coords2,num])

        Si = np.zeros((zlen,xlen,numS))
        for num in range(0,numS):
            Si[:,:,num] = si.griddata(xzplane,Splane[:,num],(xi,zi),method='cubic')

        # Replace NaNs in values that are outside the domain as zeros.
        where_are_NaNs = np.isnan(Si[:,:,num])
        Si[where_are_NaNs,num] = 0

        x_size = maxx - minx
        z_size = maxz - minz

        fig_x = 4
        fig_z = fig_x*(z_size/x_size)
        fig_x = fig_x*4.0/3.0

        fig_x = 20
        fig_z = 40

        fig = plt.figure(figsize=(fig_x,fig_z))
        ax = plt.gca()

        # Scaling
        if (scaling):
            Si = Pe**(fields[i].scale) * Si
            fields[i].limits = [ lx * Pe**(fields[i].scale) for lx in  fields[i].limits ]

        #if (fields[i].name == 'magvel'):
            #Si = np.where(Si<0,0,Si)
            #Si = np.log([x + 0.1 for x in Si])
        #    Si = np.log(Si)

        # Plotting
        if (fields[i].set_limits):
            lims = fields[i].limits
            plt.pcolor(xi,zi,Si[:,:,num],cmap=cm,vmin=lims[0],vmax=lims[1])
        else:
            plt.pcolor(xi,zi,Si[:,:,num],cmap=cm)

        if ( plot_colourbar ):
            cbar = plt.colorbar()

        plt.title("Time: {:3.3f}".format(time))
        plt.axis([minx, maxx, minz, maxz])

        font = {'family' : 'sans',
                'weight' : 'normal',
                'size'   : 36}

        plt.rc('font', **font)

        plt.draw()

        plt.savefig(os.path.join(''.join([save_name,repr(file_number).zfill(5),'.png'])),bbox_inches='tight')

    return



def head_radius( filename, order, start_file, jump, final_timestep, numelz, fields, fineness, set_zoom, zoom_vals ):

    plot_colourbar = 'yes'
    order = order - 1

    final_file = int(final_timestep/jump)
    range_vals = [x-(jump-1) for x in np.array(range(1,final_file+1))*jump]

    # Create directories for saving.
    nfields = len(fields)
    save_dir_stub = './processing/images/'
    gn.create_folders( fields, nfields, save_dir_stub, set_zoom )

    # Custom colour map.
    f = open('/home/home01/scdrw/scripts/python/processing/colour_map/full_colour_map.txt','r')
    cm_str = f.read(); cm_str = cm_str[:-1]
    cm_str = [x.split(',') for x in cm_str.split('\n')]
    cm = [[float(v)/256.0 for v in r ] for r in cm_str]
    f.close()

    cm = plt_c.ListedColormap(np.flipud(cm))

    # Reading in mesh data.
    data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename,'0.f00001']))
    Xplane,Zplane,xzplane,coords1,coords2,xi,zi,xlen,zlen,minmax,nel,gll = gn.read_mesh( data, fineness, numelz, set_zoom, zoom_vals )

    minx = minmax[0]
    maxx = minmax[1]
    minz = minmax[2]
    maxz = minmax[3]

    start_threshold = (start_file - 1)*jump
    file_counter = 0

    for k in range_vals:

        file_counter += 1 
        
        if ( k > start_threshold ):

            file_num = int((k-1)/jump + 1)

            # Outputs counter to terminal.
            files_remaining = int(final_file - k/jump + 1)
            sys.stdout.write("\r")
            sys.stdout.write("Files remaining: {:3d}".format(files_remaining))
            sys.stdout.flush()

            # Reads data files.
            data,time,istep,header,elmap,u_i,v_i,w_i,t_i,s_i = rn.readnek(''.join([filename, \
                '0.f',repr(k).zfill(5)]))

            # Run through all plot choices.
            for i in range(0,nfields):

                # Names
                name = fields[i].folder
                if (set_zoom): name = name + "_zoom"
                save_name = ''.join([save_dir_stub,name,'/',name])

                num = 0; S = np.zeros((nel,gll,1))
                if ( fields[i].name == 'vvel' ): S[:,:,0] = np.array(data[:,:,w_i])
                elif ( fields[i].name == 'hvel' ): S[:,:,0] = np.array(data[:,:,u_i])
                elif ( fields[i].name == 'ps' ): S[:,:,0] = np.array(data[:,:,s_i])
                elif ( fields[i].name == 'th' ): S[:,:,0] = np.array(data[:,:,t_i])
                elif ( fields[i].name == 'vorticity' ):
                    S = np.zeros((nel,gll,3))
                    S[:,:,0] = np.array(data[:,:,u_i])
                    S[:,:,1] = np.array(data[:,:,v_i])
                    S[:,:,2] = np.array(data[:,:,w_i])

                arrlength = np.shape(Xplane)
                arrlength = arrlength[0]

                Non,Non,numS = np.shape(S)
                
                Splane = np.zeros((arrlength,numS))

                for num in range(0,numS):
                    Splane[:,num] = np.array(S[coords1,coords2,num])

                Si = np.zeros((zlen,xlen,numS))
                for num in range(0,numS):
                    Si[:,:,num] = si.griddata(xzplane,Splane[:,num],(xi,zi),method='cubic')

                #if (plot_choice == 'th' ):
                #    S_min = 2.0
                #    Si = np.clip(Si,0,S_min)

                # Replace NaNs in values that are outside the domain as zeros.
                where_are_NaNs = np.isnan(Si[:,:,num])
                Si[where_are_NaNs,num] = 0

                #if (log_plot):
                #    Si = np.where(Si<0,0,Si)
                #    Si = np.log([x + 0.001 for x in Si])
                    
                x_size = maxx - minx
                z_size = maxz - minz

                fig_x = 15
                #fig_z = fig_x*(z_size/x_size)
                fig_x = 20
                fig_z = 40

                plt.figure(figsize=(fig_x,fig_z))

    #...........Plotting, decides whether to set c-values.
                if (fields[i].set_limits):
                    lims = fields[i].limits
#                    plt.pcolor(xi,zi,Si[:,:,num],cmap=cm,vmin=lims[0],vmax=lims[1])
                    plt.contour(xi,zi,Si[:,:,num],[0.8, 2.0],cmap=cm,vmin=lims[0],vmax=lims[1])
                else:
#                    plt.pcolor(xi,zi,Si[:,:,num],cmap=cm)
                    plt.contour(xi,zi,Si[:,:,num],[0.8, 2.0],cmap=cm)

                if (plot_colourbar == 'yes' ):
                    cbar = plt.colorbar()
                    plt.draw()

                for i in range(0,100):
                    xii = -5 + i*0.1
                    if ( xii == 0 ):
                        lw = 4
                    elif ( abs(xii) == 1 or abs(xii) == 2 or abs(xii) == 3 ):
                        lw = 4
                    elif ( abs(xii) == 0.5 or abs(xii) == 1.5 or abs(xii) == 2.5  ):
                        lw = 3
                    else:
                        lw = 1
                    plt.plot([xii,xii],[minz,maxz],'k',linewidth = lw)

                plt.title("Time: {:3.3f}".format(time))
                plt.axis([minx, maxx, minz, maxz])

                font = {'family' : 'sans',
                        'weight' : 'normal',
                        'size'   : 24}

                plt.rc('font', **font)

                plt.savefig(os.path.join(''.join([save_name,repr(file_counter).zfill(5),'.png'])),bbox_inches='tight')
                plt.close('all') 

    return
